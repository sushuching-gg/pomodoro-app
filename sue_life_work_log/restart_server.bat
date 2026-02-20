@echo off
set "PYTHON_PATH=C:\Python314\python.exe"
set "PROJECT_DIR=c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log"

cd /d "%PROJECT_DIR%"

echo [Sue's Work Log] Ensuring port 5000 is clear...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000"') do (
    echo Killing process %%a...
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo [Sue's Work Log] Starting Web Server...
"%PYTHON_PATH%" app.py

if errorlevel 1 (
    echo.
    echo ERROR: Server crashed.
    pause
)
pause
