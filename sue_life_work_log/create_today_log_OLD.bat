@echo off
setlocal

:: Gets the current date in YYYY-MM-DD format
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
:: Note: Date format depends on system locale. Trying a more robust way via PowerShell
for /f %%a in ('powershell -Command "Get-Date -format 'yyyy-MM-dd'"') do set mydate=%%a

set "FILENAME=%mydate%-daily-log.md"
set "FILEPATH=content\logs\%FILENAME%"
set "TEMPLATE=---\ntitle: Daily Log %mydate%\ndate: %mydate%\ntype: log\n---\n\n# Today's Goals\n- [ ] \n\n# Notes\n"

cd /d "c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log"

if exist "%FILEPATH%" (
    echo Log file for today already exists: %FILENAME%
) else (
    echo Creating new log file: %FILENAME%
    :: Using PowerShell to write file with UTF8 encoding to avoid encoding issues
    powershell -Command "Set-Content -Path '%FILEPATH%' -Value \"---\`ntitle: Daily Log %mydate%\`ndate: %mydate%\`ntype: log\`n---\`n\`n# Today's Goals\`n- [ ] \`n\`n# Notes\`n\" -Encoding UTF8"
)

echo Opening Editor...
start http://localhost:5000/admin/edit/logs/%FILENAME%

pause
