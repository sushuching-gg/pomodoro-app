import os
import re

filename = "sue_life_work_log/app.py"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# Simple, reliable startup print
new_print_logic = '''
    local_ip = get_local_ip()
    port = 5000
    
    print("\\n" + "="*50)
    print("SUE LOG SERVER ACTIVE")
    print("-" * 50)
    print(f"LAPTOP: http://localhost:{port}")
    print(f"MOBILE: http://100.99.205.25:{port} (Tailscale)")
    print("="*50 + "\\n")
'''

# Replace whatever mess is there now with something clean
pattern = r'if __name__ == .__main__.{1,2}:.*?app\.run'
replacement = f'if __name__ == "__main__":\\n{new_print_logic}\\n    app.run'
# Actually, the regex might be tricky due to indentation. Let's do a line-by-line rewrite for safety.

lines = content.splitlines()
new_lines = []
skip = False
for line in lines:
    if 'if __name__ == "__main__":' in line or "if __name__ == '__main__':" in line:
        new_lines.append(line)
        new_lines.append(new_print_logic)
        skip = True
        continue
    if skip:
        if "app.run" in line:
            new_lines.append(line)
            skip = False
        continue
    new_lines.append(line)

with open(filename, "w", encoding="utf-8") as f:
    f.write("\\n".join(new_lines))
