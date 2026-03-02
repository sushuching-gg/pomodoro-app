import os
import re

filename = "sue_life_work_log/app.py"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# 強度更高、自動偵測 IP 的展示邏輯
new_print_logic = '''
    local_ip = get_local_ip()
    hostname = socket.gethostname()
    port = 5000
    
    # Try to find Tailscale IP specifically
    tailscale_ip = "100.99.205.25" # Default known
    try:
        import subprocess
        ts_output = subprocess.check_output(["tailscale", "ip", "-4"]).decode().strip()
        if ts_output: tailscale_ip = ts_output
    except: pass

    print("\\n" + "="*50)
    print("[START] Sue Log Server Active")
    print("-" * 50)
    print(f"> Local View:  http://localhost:{port}")
    print(f"> Network View: http://{local_ip}:{port}")
    print(f"> Mobile View:  http://{tailscale_ip}:{port} (Tailscale)")
    print(f"> MagicDNS:    http://{hostname}.local:{port}")
    print("="*50 + "\\n")
'''

# 用 regex 替換掉原本那段 print 區域
pattern = r'local_ip = get_local_ip\(\).*?print\("="\*50 \+ "\\n"\)'
content = re.sub(pattern, new_print_logic, content, flags=re.DOTALL)

with open(filename, "w", encoding="utf-8") as f:
    f.write(content)
