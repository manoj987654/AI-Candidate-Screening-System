"""
Utility functions for the application
"""
import uuid
from datetime import datetime
from typing import List


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())


def generate_timestamp() -> datetime:
    """Generate current timestamp"""
    return datetime.now()


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks for better context preservation
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        
        if chunk.strip():
            chunks.append(chunk)
        
        start += chunk_size - overlap
    
    return chunks


def sanitize_filename(filename: str) -> str:
    """Remove special characters from filename"""
    import re
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)


def format_session_summary(session_data: dict) -> str:
    """Format session data into human-readable summary"""
    summary = f"""
Interview Session Summary
=========================
Session ID: {session_data.get('session_id')}
Role: {session_data.get('role')}
Total Questions: {session_data.get('total_questions')}
Completed At: {session_data.get('completed_at')}

Q&A Pairs:
----------
"""
    
    for i, qa in enumerate(session_data.get('qa_pairs', []), 1):
        summary += f"\n[Question {i}]\n{qa.get('question')}\n"
        summary += f"\n[Answer]\n{qa.get('answer')}\n"
    
    return summary
