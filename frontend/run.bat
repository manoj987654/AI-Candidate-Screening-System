@echo off
REM Windows run script for Frontend development server

echo.
echo ================================================================================
echo   AI-Powered Candidate Screening System - Frontend
echo ================================================================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed
    echo.
)

echo.
echo ================================================================================
echo   Starting Development Server
echo ================================================================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo.
echo Make sure the backend server is running on port 8000
echo Press CTRL+C to stop the server
echo.
echo ================================================================================
echo.

REM Start development server
call npm run dev

pause
