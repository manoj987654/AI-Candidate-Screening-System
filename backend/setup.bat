@echo off
REM Windows setup script for AI-Powered Candidate Screening System

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo   AI-Powered Candidate Screening System - Windows Setup
echo ================================================================================
echo.

REM Check Python version
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    if exist ".env.example" (
        copy .env.example .env
        echo .env file created from .env.example
    ) else (
        echo WARNING: .env.example not found
    )
) else (
    echo .env file already exists
)
echo.

REM Create directories
if not exist "sessions" mkdir sessions
if not exist "vector_db" mkdir vector_db
if not exist "logs" mkdir logs
echo Directories created
echo.

echo ================================================================================
echo   Setup Complete!
echo ================================================================================
echo.
echo Next steps:
echo.
echo 1. Edit .env file and add your OpenAI API key:
echo    OPENAI_API_KEY=sk-your-actual-key-here
echo.
echo 2. Ingest knowledge base:
echo    python ingest_knowledge.py
echo.
echo 3. Start the server:
echo    python run.py
echo.
echo 4. In another terminal, start the frontend:
echo    cd ..\frontend
echo    npm install
echo    npm run dev
echo.
echo 5. Open browser and visit:
echo    http://localhost:5173
echo.
pause
