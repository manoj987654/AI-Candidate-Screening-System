from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
import logging
from datetime import datetime

from app.services import (
    ResumeParser,
    SessionManager,
    RAGService,
    QuestionGenerator
)

from app.models.schema import CandidateAnswerRequest
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------
# Initialize Services
# ---------------------------------------------------

session_manager = SessionManager()
rag_service = RAGService(settings.vector_db_path)
question_generator = QuestionGenerator(settings.openai_api_key)


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@router.get("/health")
async def health_check():

    return JSONResponse(
        {
            "status": "healthy",
            "service": "Candidate Screening API",
            "version": "1.0.0"
        }
    )


# ---------------------------------------------------
# Start Interview Session
# ---------------------------------------------------

@router.post("/api/sessions/start")
async def start_session(role: str):

    if not role:
        raise HTTPException(
            status_code=400,
            detail="Role is required"
        )

    session_id = str(uuid.uuid4())

    logger.info(
        f"Created Session {session_id} for {role}"
    )

    return JSONResponse(
        {
            "session_id": session_id,
            "role": role,
            "status": "ready_for_resume"
        }
    )


# ---------------------------------------------------
# Upload Resume
# ---------------------------------------------------

@router.post("/api/resume/upload")
async def upload_resume(
    session_id: str,
    resume_file: UploadFile = File(...),
    role: str = None
):

    try:

        if not session_id:
            raise HTTPException(
                status_code=400,
                detail="Session ID required"
            )

        if not role:
            raise HTTPException(
                status_code=400,
                detail="Role required"
            )

        logger.info(
            f"Uploading resume for session {session_id}"
        )

        filename = resume_file.filename.lower()

        if not (
            filename.endswith(".pdf")
            or filename.endswith(".txt")
        ):
            raise HTTPException(
                status_code=400,
                detail="Resume must be PDF or TXT"
            )

        content = await resume_file.read()

        if filename.endswith(".pdf"):
            resume_text = ResumeParser.extract_from_pdf(content)
        else:
            resume_text = content.decode(
                "utf-8",
                errors="ignore"
            )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Resume is empty"
            )

        resume_data = ResumeParser.parse_resume(
            resume_text
        )

        session_manager.create_session(
            session_id,
            role,
            resume_data
        )

        logger.info(
            f"Resume processed successfully ({session_id})"
        )

        return JSONResponse(
            {
                "session_id": session_id,
                "message": "Resume uploaded successfully",
                "extracted_data": {
                    "skills": resume_data["skills"],
                    "technologies": resume_data["technologies"],
                    "domain_exposure": resume_data["domain_exposure"],
                    "character_count": len(resume_text)
                }
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ---------------------------------------------------
# Get Next Interview Question
# ---------------------------------------------------

@router.post("/api/interview/next-question")
async def get_next_question(session_id: str):
    """
    Generate the next interview question.
    """

    try:

        if not session_id:
            raise HTTPException(
                status_code=400,
                detail="Session ID is required"
            )

        logger.info(f"Getting next question for {session_id}")

        # -----------------------------
        # Get Session
        # -----------------------------

        session = session_manager.get_session(session_id)

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        # -----------------------------
        # Build Retrieval Queries
        # -----------------------------

        retrieval_queries = rag_service.construct_retrieval_queries(
            session.resume_data.model_dump(),
            session.role
        )

        all_context = []

        for query in retrieval_queries:

            try:

                context = rag_service.retrieve_context(
                    session.role,
                    query,
                    top_k=2
                )

                all_context.extend(context)

            except Exception as e:

                logger.warning(
                    f"Retrieval failed: {str(e)}"
                )

        # -----------------------------
        # Remove Duplicate Context
        # -----------------------------

        unique_context = []

        seen = set()

        for item in all_context:

            if item not in seen:
                unique_context.append(item)
                seen.add(item)

        logger.info(
            f"Retrieved {len(unique_context)} context chunks"
        )

        # -----------------------------
        # Previous Questions
        # -----------------------------

        previous_questions = [
            qa.question
            for qa in session.qa_pairs
            if qa.question
        ]

        logger.info(
            f"Questions already asked: {len(previous_questions)}"
        )

        # -----------------------------
        # Generate Question
        # -----------------------------

        questions = question_generator.generate_questions(
            role=session.role,
            retrieved_context=unique_context,
            resume_data=session.resume_data.model_dump(),
            previous_questions=previous_questions,
            num_questions=1
        )

        if not questions:

            logger.warning(
                "Question generator returned nothing."
            )

            questions = [
                "Tell me about the most challenging technical project you've worked on."
            ]

        question = questions[0]

        # Save current question
        session.current_question = question
        session.updated_at=datetime.now()
        session_manager._save_session(session)


        question_number = len(session.qa_pairs) + 1

        logger.info(
            f"Generated Question {question_number}: {question}"
        )

        return JSONResponse(
            {
                "session_id": session_id,
                "question_number": question_number,
                "question": question,
                "retrieved_context": unique_context
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        logger.error(
            f"Question generation failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ---------------------------------------------------
# Submit Candidate Answer
# ---------------------------------------------------

@router.post("/api/interview/submit-answer")
async def submit_answer(answer_request: CandidateAnswerRequest):
    """
    Store candidate answer and update interview history.
    """

    try:

        if not answer_request.session_id:
            raise HTTPException(
                status_code=400,
                detail="Session ID is required"
            )

        if not answer_request.answer.strip():
            raise HTTPException(
                status_code=400,
                detail="Answer cannot be empty"
            )

        # -----------------------------------
        # Get Session
        # -----------------------------------

        session = session_manager.get_session(
            answer_request.session_id
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        logger.info(
            f"Saving answer for Question {answer_request.question_number}"
        )

        # -----------------------------------
        # Save Q&A Pair
        # -----------------------------------

        qa_data = {
            "question_number": answer_request.question_number,
            "question": answer_request.question,
            "retrieved_context": [],
            "answer": answer_request.answer,
            "timestamp": datetime.now()
        }

        success = session_manager.add_qa_pair(
            answer_request.session_id,
            qa_data
        )
        session = session_manager.get_session(answer_request.session_id)

        print("QA COUNT =", len(session.qa_pairs))

        if not success:
            raise Exception("add_qa_pair returned False")

        logger.info(
            f"Interview now contains {len(session.qa_pairs)} question(s)"
        )

        # Clear current question
        #session.current_question = None
        session.updated_at = datetime.now()
        session_manager._save_session(session)

        return JSONResponse(
            {
                "status": "success",
                "message": "Answer recorded successfully",
                "question_number": answer_request.question_number,
                "total_questions_answered": len(session.qa_pairs)
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )