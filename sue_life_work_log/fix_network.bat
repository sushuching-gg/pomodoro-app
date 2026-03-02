@echo off
echo [Sue Log Network Fix] Fixing mobile connection...
echo.
echo [1/2] Checking Firewall...
netsh advfirewall firewall show rule name="Flask Port 5000" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Rule not found, creating (Requires Admin)...
    netsh advfirewall firewall add rule name="Flask Port 5000" dir=in action=allow protocol=TCP localport=5000
    if %errorlevel% neq 0 (
        echo [ERROR] Failed! Please right-click and "Run as Administrator".
        pause
        exit /b %errorlevel%
    )
    echo [OK] Firewall rule created.
) else (
    echo [OK] Firewall rule exists.
)

echo.
echo [2/2] Access URLs...
hostname > temp.txt
set /p host=<temp.txt
del temp.txt
echo ==========================================
echo Consistent Access URLs:
echo PC: http://localhost:5000
echo Mobile: http://%host%.local:5000
echo ==========================================
echo TIP: Save the Mobile URL to your bookmarks.
echo.
pause