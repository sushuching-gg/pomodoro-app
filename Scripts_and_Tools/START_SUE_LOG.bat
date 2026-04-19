@echo off
:: Set paths
set "PYTHON_EXE=C:\Python314\python.exe"
set "APP_DIR=%~dp0sue_life_work_log"

echo ========================================
echo   Sue Log Server: Starting...
echo ========================================

:: Change to app directory
cd /d "%APP_DIR%"

:: Kill any old processes on port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000"') do (
    taskkill /f /pid %%a >nul 2>&1
)

:: Run the server
"%PYTHON_EXE%" app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server failed to start or crashed.
    pause
)
pause
