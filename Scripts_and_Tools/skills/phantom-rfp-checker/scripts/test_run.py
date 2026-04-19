#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速測試: 用嘉義縣需求說明書跑一次檢核"""
import os, sys, json

# 找到嘉義縣需求說明書
INDEX = r'c:\Users\user\.gemini\antigravity\brain\My_AI_Project\skills\phantom-file-navigator\scripts\file_index.json'
with open(INDEX, 'r', encoding='utf-8') as f:
    idx = json.load(f)

target_file = None
for item in idx:
    if item['name'] == '嘉義縣需求說明書.docx':
        target_file = item['path']
        break

if not target_file:
    print("找不到嘉義縣需求說明書.docx")
    sys.exit(1)

print(f"目標檔案: {target_file}")

# 模擬命令列呼叫
sys.argv = ['rfp_checker.py', target_file]

# 匯入並執行
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import rfp_checker
rfp_checker.main()
