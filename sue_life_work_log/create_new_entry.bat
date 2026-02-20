@echo off
setlocal EnableDelayedExpansion

:: Set utf-8 encoding
chcp 65001 >nul

echo ==========================================
echo      Sue's Life & Work Log Creator
echo ==========================================
echo 1. Work Log (工作日誌)
echo 2. Life: Me (我的生活)
echo 3. Life: Grandma (阿嬤的生活)
echo 4. Life: Travel (旅遊紀錄)
echo ==========================================
set /p choice="Please select (1-4): "

if "%choice%"=="1" (
    set "CATEGORY=work"
    set "TYPE_NAME=Work Log"
    set "DIR_PATH=content\work"
) else if "%choice%"=="2" (
    set "CATEGORY=life_daily_me"
    set "TYPE_NAME=Life Log (Me)"
    set "DIR_PATH=content\life\daily\me"
) else if "%choice%"=="3" (
    set "CATEGORY=life_daily_grandma"
    set "TYPE_NAME=Life Log (Grandma)"
    set "DIR_PATH=content\life\daily\grandma"
) else if "%choice%"=="4" (
    set "CATEGORY=life_travel"
    set "TYPE_NAME=Travel Log"
    set "DIR_PATH=content\life\travel"
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b
)

:: Get Date
for /f %%a in ('powershell -Command "Get-Date -format 'yyyy-MM-dd'"') do set mydate=%%a
set "FILENAME=%mydate%-%CATEGORY%.md"
set "FILEPATH=%DIR_PATH%\%FILENAME%"

cd /d "c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log"

if exist "%FILEPATH%" (
    echo.
    echo [INFO] File already exists: %FILENAME%
) else (
    echo.
    echo [NEW] Creating file: %FILENAME%
    powershell -Command "Set-Content -Path '%FILEPATH%' -Value \"---\`ntitle: %mydate% %TYPE_NAME%\`ndate: %mydate%\`ntype: %CATEGORY%\`n---\`n\`n# Notes\`n\" -Encoding UTF8"
)

echo Opening Editor...
start http://localhost:5000/admin/edit/%CATEGORY%/%FILENAME%

pause
