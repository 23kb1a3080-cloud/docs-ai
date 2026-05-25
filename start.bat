@echo off
echo ========================================
echo   Starting DocMind AI
echo ========================================
echo.

echo Starting Backend Server...
start "DocMind AI - Backend" cmd /k "cd backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
start "DocMind AI - Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   DocMind AI Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/api/docs
echo.
echo Opening application in browser...
timeout /t 5 /nobreak >nul
start http://localhost:3000
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WindowTitle eq DocMind AI - Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq DocMind AI - Frontend*" /T /F >nul 2>&1
echo Servers stopped.
