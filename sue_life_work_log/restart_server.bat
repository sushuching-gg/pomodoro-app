@echo off
set "PYTHON_PATH=C:\Python314\python.exe"
set "PROJECT_DIR=c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log"

cd /d "%PROJECT_DIR%"

echo.
echo ==========================================
echo [Sue's Work Log] Server Startup
echo ==========================================
echo.

echo [1/2] Cleaning up Port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000"') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo [2/2] Starting Flask Server...
echo.
echo TIP: If mobile cannot connect, run fix_network.bat first.
echo.

"%PYTHON_PATH%" app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server stopped unexpectedly.
    pause
)
pause