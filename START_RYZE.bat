@echo off
title Ryze AI - 1-Click Launch
cls
echo ========================================================
echo        Ryze AI: Ultimate UI Generator
echo ========================================================
echo.

echo [1/3] Ensuring Frontend Cache & Styles...
cd frontend
if not exist "node_modules" (
    echo    - Installing Frontend specific packages...
    call npm install
    call npm install -D tailwindcss@3.4.17 postcss autoprefixer
)
cd ..

echo [2/3] Verifying Backend Dependencies...
cd backend
if not exist "node_modules" call npm install
cd ..

echo [3/3] Verifying AI Dependencies...
cd ai-service
if not exist "venv" (
    echo    - Setting up Python Environment...
    pip install -r requirements.txt
)
cd ..

echo.
echo ========================================================
echo   Launch Sequence Initiated. 
echo   Please wait for the Browser to open at http://localhost:5173
echo ========================================================
echo.

start "" "http://localhost:5173"
npm run dev
pause
