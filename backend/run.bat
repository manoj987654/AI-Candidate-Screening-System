@echo off
REM Windows run script for AI-Powered Candidate Screening System Backend

echo.
echo ================================================================================
echo   AI-Powered Candidate Screening System - Backend Server
echo ================================================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if knowledge base exists
if not exist "vector_db" (
    echo WARNING: Knowledge base directory not found
    echo Run: python ingest_knowledge.py
    echo.
)

echo.
echo ================================================================================
echo   Starting Backend Server
echo ================================================================================
echo.
echo API Server:  http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Redoc:       http://localhost:8000/redoc
echo.
echo Press CTRL+C to stop the server
echo.
echo ================================================================================
echo.

REM Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
