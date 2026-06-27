#!/usr/bin/env python
"""
Run the backend server
"""
import os
import sys
import subprocess
import platform

# Add current directory to path
sys.path.insert(0, '.')

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run: python setup.py")
        sys.exit(1)

def check_openai_key():
    """Check if OpenAI key is set"""
    from app.core.config import settings
    
    if not settings.openai_api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not set in .env")
        print("Without this, question generation will fall back to rule-based method")
        print("To use GPT-3.5 for better questions, add your key to .env")
        print()

def check_knowledge_base():
    """Check if knowledge base is initialized"""
    vector_db_path = "./vector_db"
    
    if not os.path.exists(vector_db_path) or len(os.listdir(vector_db_path)) == 0:
        print("⚠️  WARNING: Knowledge base not initialized!")
        print("Please run: python ingest_knowledge.py")
        print("This will initialize the vector database with role-specific knowledge")
        print()

def main():
    """Start the server"""
    print("\n" + "=" * 80)
    print("  Starting AI-Powered Candidate Screening System Backend")
    print("=" * 80 + "\n")
    
    try:
        check_env_file()
        check_openai_key()
        check_knowledge_base()
        
        print("Starting Uvicorn server...\n")
        print("🚀 API Server:  http://localhost:8000")
        print("📚 API Docs:    http://localhost:8000/docs")
        print("⚙️  Redoc:       http://localhost:8000/redoc")
        print("\nPress CTRL+C to stop the server\n")
        print("=" * 80 + "\n")
        
        # Start uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
