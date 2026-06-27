from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App settings
    app_name: str = "Candidate Screening System"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/candidate_screening"
    
    # API Keys
    openai_api_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-this"
    
    # Vector DB
    vector_db_path: str = "./vector_db"
    
    # Interview settings
    default_questions_per_session: int = 5
    interview_timeout_minutes: int = 30
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
