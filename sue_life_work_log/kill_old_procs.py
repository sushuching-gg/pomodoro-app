import os
import psutil

# Force kill any unexpected rogue Flask processes by port
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmdline = proc.cmdline()
        if "python" in proc.name() and "app.py" in str(cmdline):
            print(f"Killing old app.py process: {proc.pid}")
            proc.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
