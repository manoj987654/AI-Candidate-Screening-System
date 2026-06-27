import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [currentStep, setCurrentStep] = useState('role-selection') // role-selection, resume-upload, interview, results
  const [selectedRole, setSelectedRole] = useState(null)
  const [resumeFile, setResumeFile] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [currentAnswer, setCurrentAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const roles = [
    { id: 'ml-engineer', name: 'ML Engineer', description: 'Machine Learning Engineer' },
    { id: 'backend-engineer', name: 'Backend Engineer', description: 'Backend Software Engineer' },
    { id: 'data-scientist', name: 'Data Scientist', description: 'Data Science & Analytics' }
  ]

  const handleStartSession = async (role) => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.post(
  '/api/sessions/start',
  null,
  {
    params: {
      role: role
    }
  }
);
console.log("Start Session Response:", response.data);
      setSessionId(response.data.session_id)
      setSelectedRole(role)
      setCurrentStep('resume-upload')
    } catch (err) {
      setError('Failed to start session: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleResumeUpload = async (e) => {
    e.preventDefault()
    
    if (!resumeFile) {
      setError('Please select a resume file')
      return
    }

    try {
      setLoading(true)
      setError(null)
      
      const formData = new FormData()
      formData.append('resume_file', resumeFile)
      console.log("Session ID:", sessionId)
  console.log("Selected Role:", selectedRole)
      

      const response = await axios.post(
  "/api/resume/upload",
  formData,
  {
    params: {
      session_id: sessionId,
      role: selectedRole
    },
    headers: {
      "Content-Type": "multipart/form-data"
    }
  }
);
      setCurrentStep('interview')
      await getNextQuestion()
    } catch (err) {
  console.log(err.response.data);
  alert(JSON.stringify(err.response.data));
} finally {
      setLoading(false)
    }
  }

  const getNextQuestion = async () => {
    try {
      setLoading(true)
      const response = await axios.post(`/api/interview/next-question?session_id=${sessionId}`)
      setCurrentQuestion(response.data)
      setCurrentAnswer('')
    } catch (err) {
      setError('Failed to get next question: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitAnswer = async (e) => {
    e.preventDefault()
    
    if (!currentAnswer.trim()) {
      setError('Please provide an answer')
      return
    }

    try {
      setLoading(true)
      setError(null)

      await axios.post('/api/interview/submit-answer', {
        session_id: sessionId,
        question_number: currentQuestion.question_number,
        question: currentQuestion.question,
        answer: currentAnswer
      })

      // Continue to next question or end interview
      if (currentQuestion.question_number < 3) { // Example: 3 questions per session
        await getNextQuestion()
      } else {
        setCurrentStep('results')
      }
    } catch (err) {
      console.log(err.response.data);
      alert(JSON.stringify(err.response.data));
    } finally {
      setLoading(false)
    }
  }

  const getSessionSummary = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`/api/sessions/${sessionId}/summary`)
      return response.data
    } catch (err) {
      setError('Failed to get session summary: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <header className="header">
        <h1>AI-Powered Candidate Screening System</h1>
        <p>Role-based Technical Interview Platform</p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="container">
        {currentStep === 'role-selection' && (
          <div className="step role-selection">
            <h2>Select Target Role</h2>
            <div className="roles-grid">
              {roles.map(role => (
                <button
                  key={role.id}
                  className="role-card"
                  onClick={() => handleStartSession(role.id)}
                  disabled={loading}
                >
                  <h3>{role.name}</h3>
                  <p>{role.description}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {currentStep === 'resume-upload' && (
          <div className="step resume-upload">
            <h2>Upload Your Resume</h2>
            <form onSubmit={handleResumeUpload}>
              <div className="form-group">
                <label htmlFor="resume">Resume File (PDF or TXT)</label>
                <input
                  type="file"
                  id="resume"
                  accept=".pdf,.txt"
                  onChange={(e) => setResumeFile(e.target.files[0])}
                  disabled={loading}
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Processing...' : 'Upload and Start Interview'}
              </button>
            </form>
          </div>
        )}

        {currentStep === 'interview' && currentQuestion && (
          <div className="step interview">
            <div className="question-progress">
              Question {currentQuestion.question_number}
            </div>
            <h2>{currentQuestion.question}</h2>
            <form onSubmit={handleSubmitAnswer}>
              <div className="form-group">
                <label htmlFor="answer">Your Answer</label>
                <textarea
                  id="answer"
                  value={currentAnswer}
                  onChange={(e) => setCurrentAnswer(e.target.value)}
                  disabled={loading}
                  rows="6"
                  placeholder="Type your answer here..."
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Submitting...' : 'Submit Answer'}
              </button>
            </form>
          </div>
        )}

        {currentStep === 'results' && (
          <div className="step results">
            <h2>Interview Complete!</h2>
            <p>Thank you for completing the interview. Your responses have been recorded.</p>
            <button onClick={() => window.location.reload()}>Start New Interview</button>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
