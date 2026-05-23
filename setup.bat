@echo off
REM DocMind AI - Setup Script for Windows
REM This script helps you set up the project quickly

echo.
echo ================================
echo DocMind AI - Setup Script
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed
    echo Please install Python 3.11 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed
    echo Please install Node.js 18 or higher from nodejs.org
    pause
    exit /b 1
)

echo [OK] Node.js found
node --version

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed
    pause
    exit /b 1
)

echo [OK] npm found
npm --version

echo.
echo ================================
echo Setting up Backend...
echo ================================
echo.

REM Backend setup
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Python dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo [WARNING] Please edit backend\.env with your API keys
) else (
    echo [WARNING] .env file already exists
)

cd ..

echo.
echo ================================
echo Setting up Frontend...
echo ================================
echo.

REM Frontend setup
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install
echo [OK] Node.js dependencies installed

REM Create .env.local file if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local file...
    copy .env.example .env.local
    echo [OK] .env.local created
) else (
    echo [WARNING] .env.local file already exists
)

cd ..

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next Steps:
echo.
echo 1. Configure API Keys:
echo    - Edit backend\.env with your:
echo      * OPENAI_API_KEY or GEMINI_API_KEY
echo      * GITHUB_TOKEN
echo      * DATABASE_URL (optional, defaults to SQLite)
echo.
echo 2. Start the Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 3. Start the Frontend (in a new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open your browser:
echo    http://localhost:3000
echo.
echo Documentation:
echo    - Quick Start: QUICKSTART.md
echo    - Full Docs: docs\
echo.
echo Happy coding!
echo.
pause
