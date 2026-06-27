import json
import os
import logging
import traceback
from datetime import datetime
from typing import List, Optional
from app.models.schema import InterviewSession, QAPair, ResumeData

logger = logging.getLogger(__name__)


class SessionManager:
    """Service to manage interview sessions with file-based persistence"""
    
    def __init__(self, session_storage_path: str = "./sessions"):
        """
        Initialize session manager
        
        Args:
            session_storage_path: Directory to store session JSON files
        """
        self.session_storage_path = session_storage_path
        os.makedirs(session_storage_path, exist_ok=True)
        logger.info(f"SessionManager initialized with path: {session_storage_path}")
    
    def create_session(self, session_id: str, role: str, resume_data: dict) -> InterviewSession:
        """
        Create a new interview session
        
        Args:
            session_id: Unique session identifier
            role: Target job role
            resume_data: Parsed resume information
            
        Returns:
            Created InterviewSession object
        """
        try:
            resume = ResumeData(**resume_data)
            
            session = InterviewSession(
                session_id=session_id,
                role=role,
                resume_data=resume,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status="active"
            )
            
            self._save_session(session)
            logger.info(f"Session created: {session_id} for role: {role}")
            return session
        except Exception as e:
            logger.error(f"Failed to create session {session_id}: {str(e)}")
            raise
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """
        Retrieve an existing session
        
        Args:
            session_id: Session identifier
            
        Returns:
            InterviewSession object or None if not found
        """
        try:
            session_file = os.path.join(self.session_storage_path, f"{session_id}.json")
            
            if not os.path.exists(session_file):
                logger.warning(f"Session not found: {session_id}")
                return None
            
            with open(session_file, 'r') as f:
                data = json.load(f)
            
            # Reconstruct datetime objects
            data['created_at'] = datetime.fromisoformat(data['created_at'])
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
            
            # Reconstruct QAPair timestamps
            for qa in data.get('qa_pairs', []):
                if 'timestamp' in qa and qa['timestamp']:
                    qa['timestamp'] = datetime.fromisoformat(qa['timestamp'])
            
            return InterviewSession(**data)
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {str(e)}")
            return None
    
    def add_qa_pair(self, session_id: str, qa_pair: dict) -> bool:
        """
        Add a Q&A pair to session
        
        Args:
            session_id: Session identifier
            qa_pair: Dictionary with question, answer, context
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = self.get_session(session_id)
            
            if not session:
                logger.error(f"Session not found for Q&A pair: {session_id}")
                return False
            
            # Ensure timestamp is set
            if 'timestamp' not in qa_pair or qa_pair['timestamp'] is None:
                qa_pair['timestamp'] = datetime.now()
            print("QA_PAIR =", qa_pair)
            print("CURRENT SESSION =", session)
            qa = QAPair(**qa_pair)
            session.qa_pairs.append(qa)
            session.updated_at = datetime.now()
            
            self._save_session(session)
            logger.info(f"Q&A pair added to session {session_id}, total: {len(session.qa_pairs)}")
            return True
        except Exception as e:
            import traceback

            print("\n========== ERROR IN add_qa_pair ==========")
            traceback.print_exc()
            print("QA DATA =", qa_pair)
            print("==========================================\n")

            raise
    
    def update_session_status(self, session_id: str, status: str) -> bool:
        """
        Update session status (active, completed, abandoned)
        
        Args:
            session_id: Session identifier
            status: New status value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = self.get_session(session_id)
            
            if not session:
                logger.error(f"Session not found for status update: {session_id}")
                return False
            
            session.status = status
            session.updated_at = datetime.now()
            
            self._save_session(session)
            logger.info(f"Session {session_id} status updated to: {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update session status {session_id}: {str(e)}")
            return False
    
    def _save_session(self, session: InterviewSession) -> None:
        """
        Save session to JSON file
        
        Args:
            session: InterviewSession object to save
        """
        session_file = os.path.join(self.session_storage_path, f"{session.session_id}.json")
        
        try:
            with open(session_file, 'w') as f:
                json.dump(
                    session.model_dump(mode='json'),
                    f,
                    indent=2,
                    default=str
                )
            logger.debug(f"Session saved: {session_file}")
        except Exception as e:
            logger.error(f"Failed to save session {session.session_id}: {str(e)}")
            raise
    
    def list_sessions(self) -> List[str]:
        """
        List all session IDs
        
        Returns:
            List of session identifiers
        """
        try:
            if not os.path.exists(self.session_storage_path):
                return []
            
            session_files = os.listdir(self.session_storage_path)
            sessions = [f.replace('.json', '') for f in session_files if f.endswith('.json')]
            logger.debug(f"Found {len(sessions)} sessions")
            return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions: {str(e)}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session (for cleanup)
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session_file = os.path.join(self.session_storage_path, f"{session_id}.json")
            
            if os.path.exists(session_file):
                os.remove(session_file)
                logger.info(f"Session deleted: {session_id}")
                return True
            
            logger.warning(f"Session file not found for deletion: {session_id}")
            return False
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {str(e)}")
            return False
