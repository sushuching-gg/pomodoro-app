#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
114年度招標需求書檢核器 (專屬入口)
==================================
自動連結核心引擎並套用 114 年檢核規則。
"""

import os
import sys
import subprocess

def main():
    # 1. 取得路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    # 核心引擎路徑
    engine_path = os.path.join(project_root, "skills", "phantom-rfp-checker", "scripts", "rfp_checker.py")
    # 114 規則路徑
    rules_path = os.path.join(project_root, "skills", "phantom-rfp-checker", "rules", "mandatory_sections_114.json")
    
    if not os.path.exists(engine_path):
        print(f"[錯誤] 找不到核心引擎：{engine_path}")
        return

    # 2. 處理參數
    args = sys.argv[1:]
    if len(args) < 2:
        print("用法: python rfp_checker.py <需求書.docx> <計畫書.docx> [輸出檔名.xlsx]")
        return

    rfp_file = args[0]
    plan_file = args[1]
    output_xlsx = args[2] if len(args) > 2 else "114年度_檢核分析報告_整合版.xlsx"
    
    # 預設輸出到桌面
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", output_xlsx)

    # 3. 呼叫核心引擎並強制指定 114 規則
    cmd = [
        sys.executable, engine_path,
        "--rfp", rfp_file,
        "--plan", plan_file,
        "--rules", rules_path,
        "--output", desktop_path
    ]
    
    print(f"[啟動] 正在套用 114 年度規則進行【計畫 vs. 招標】深層對照檢核...")
    try:
        subprocess.run(cmd, check=True)
        print(f"[成功] 報告已產出至：{desktop_path}")
    except subprocess.CalledProcessError:
        print(f"[錯誤] 檢核執行失敗。")
    except Exception as e:
        print(f"[錯誤] 發生非預期錯誤: {e}")

if __name__ == "__main__":
    main()
