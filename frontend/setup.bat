@echo off
REM Windows setup script for Frontend

echo.
echo ================================================================================
echo   AI-Powered Candidate Screening System - Frontend Setup
echo ================================================================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

node --version
npm --version
echo.

REM Install dependencies
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed
) else (
    echo node_modules already exists
)
echo.

echo ================================================================================
echo   Setup Complete!
echo ================================================================================
echo.
echo Run the development server with:
echo   npm run dev
echo.
pause
