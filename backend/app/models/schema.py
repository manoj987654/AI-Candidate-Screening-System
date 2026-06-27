from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoleSelection(BaseModel):
    """Role selection model"""
    role: str = Field(..., description="Target job role")
    description: Optional[str] = None


class ResumeUploadRequest(BaseModel):
    """Resume upload request"""
    session_id: str
    resume_text: str
    role: str


class ResumeData(BaseModel):
    """Extracted resume data"""
    skills: List[str] = []
    technologies: List[str] = []
    domain_exposure: List[str] = []
    raw_text: str


class QuestionResponse(BaseModel):
    """Interview question response"""
    session_id: str
    question_number: int
    question: str
    context: Optional[str] = None
    retrieved_context: Optional[List[str]] = None


class CandidateAnswerRequest(BaseModel):
    """Candidate answer submission"""
    session_id: str
    question_number: int
    question:str
    answer: str


class QAPair(BaseModel):
    """Question-Answer pair stored in session"""
    question_number: int
    question: str
    retrieved_context: List[str]
    answer: str
    timestamp: datetime


class InterviewSession(BaseModel):
    """Interview session metadata"""
    session_id: str
    candidate_name: Optional[str] = None
    role: str
    resume_data: ResumeData
    created_at: datetime
    updated_at: datetime
    status: str = "active"  # active, completed, abandoned
    qa_pairs: List[QAPair] = Field(default_factory=list)
    current_question: Optional[str] = None


class SessionSummary(BaseModel):
    """Summary of completed interview session"""
    session_id: str
    role: str
    total_questions: int
    duration_seconds: float
    qa_pairs: List[QAPair]
    completion_time: datetime
    summary: Optional[str] = None
