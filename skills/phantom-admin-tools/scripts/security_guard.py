import os
import sys

PRIMARY_MEMORY_PATH = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\PROJECT_MEMORY.md"
KEYWORDS = ["搜尋紅線", "Search Redlines", "套件白名單", "Package Whitelist", "絕對禁區", "Forbidden Zone"]

def run_guard():
    print("\n[SECURITY GUARD CHECK]")
    if not os.path.exists(PRIMARY_MEMORY_PATH):
        print("FAILED: Memory file missing")
        sys.exit(1)
    
    with open(PRIMARY_MEMORY_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        # 只要有一組中英文關鍵字存在即可通過，增加容錯性
        match_count = sum(1 for k in KEYWORDS if k in content)
        if match_count >= 3:
            print("Status: APPROVED")
            print("Standard: V3.1 (Stabilized)")
        else:
            print(f"FAILED: Incomplete integrity (Matches: {match_count})")
            sys.exit(1)
    print("-" * 20 + "\n")

if __name__ == "__main__":
    run_guard()
