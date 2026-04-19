"""
sanitizer.py - 資料去識別化腳本 (V2.1 強化版)
=============================================
優化內容：
1. 強化 114 年度專案縮寫掃描 (NTSU, 114-xxxx 等)。
2. 新增「職稱感應」偵測 (計畫主持人、委員等後的姓名自動提取)。
3. 擴展敏感機構關鍵字。
4. 優化 Mapping 邏輯以防止代碼重複雜湊。

# ══════════════════════════════════════════
# 【套件透明清單】本腳本使用以下套件，均在 PROJECT_MEMORY.md 白名單內
# 標準庫（Python 內建）：argparse, hashlib, json, os, re, shutil, datetime, pathlib
# 第三方套件：pandas, openpyxl
# 安裝指令：pip install pandas openpyxl
# ══════════════════════════════════════════
"""

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# 第三方套件 (已確認在白名單)
import pandas as pd


# ──────────────────────────────────────────────
# 區塊一：預設敏感詞彙與識別規則
# ──────────────────────────────────────────────

# 縣市對照
DEFAULT_CITIES = [
    "臺北市", "台北市", "新北市", "桃園市", "臺中市", "台中市",
    "臺南市", "台南市", "高雄市", "基隆市", "新竹市", "嘉義市",
    "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣",
    "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "台東縣",
    "澎湖縣", "金門縣", "連江縣",
]

# 機構關鍵字 (強化版)
DEFAULT_ORG_KEYWORDS = [
    "市政府", "縣政府", "體育處", "教育處", "運動局",
    "大學", "學校", "協會", "基金會", "中心", "處", "局",
    "室", "所", "署", "本部", "分會", "實驗室", "國訓"
]

# 職稱感應規則 (Context-aware rules)
# 模式：(職稱關鍵字) + [選擇性標點/空白] + (姓名(2-4字))
TITLE_CONTEXT_PATTERNS = [
    r"(?:計畫主持人|主持人|協同主持人|聯絡人|承辦人|委員|評審|老師|教授|主任|處長|局長|組長|經理)[:：\s]*([\u4e00-\u9fa5]{2,4})",
    r"([\u4e00-\u9fa5]{2,4})[:：\s]*(?:代表|簽章|收|啟)",
]

# 年度專案編號格式
PROJECT_ID_PATTERNS = [
    r"11[345]-\w+-\d+", # 如 114-NTSU-001
    r"NTSU-\d+",
    r"SPORTS-TECH-\d+",
]

# 個資正規表達式 (自動清洗不需建立對照表)
REGEX_RULES = [
    (r"[A-Z][12]\d{8}", "[ID_REDACTED]"),
    (r"09\d{2}[-\s]?\d{3}[-\s]?\d{3}", "[PHONE_REDACTED]"),
    (r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", "[EMAIL_REDACTED]"),
    (r"\(0\d{1,2}\)\s?\d{3,4}[-\s]?\d{4}", "[TEL_REDACTED]"),
]


# ──────────────────────────────────────────────
# 區塊二：核心工具函式
# ──────────────────────────────────────────────

def generate_hash_code(real_name: str, prefix: str, salt: str) -> str:
    """產生 4 碼隨機雜湊代碼"""
    raw = f"{salt}::{real_name}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:4]
    return f"[{prefix}_{digest}]"


def extract_potential_entities(texts: list[str]) -> set[str]:
    """利用語意感應提取潛在的人名與專案 ID"""
    potential_names = set()
    combined_text = "\n".join(str(t) for t in texts)
    
    # 提取職稱後的人名
    for pattern in TITLE_CONTEXT_PATTERNS:
        matches = re.findall(pattern, combined_text)
        for m in matches:
            if m: potential_names.add(m.strip())
            
    # 提取符合格式的專案 ID
    for pattern in PROJECT_ID_PATTERNS:
        matches = re.findall(pattern, combined_text)
        for m in matches:
            if m: potential_names.add(m.strip())
            
    return potential_names


def build_mapping(texts: list[str], custom_entities: dict, salt: str) -> tuple[dict, dict]:
    """掃描文字，建立代碼與真實名稱的對照表"""
    mapping = {}
    reverse = {}

    potential_entities = extract_potential_entities(texts)
    
    # 合併所有候選名詞
    cities = DEFAULT_CITIES + custom_entities.get("cities", [])
    persons = list(potential_entities) + custom_entities.get("persons", [])
    orgs = custom_entities.get("orgs", [])

    combined_text = "\n".join(str(t) for t in texts)

    # 處理縣市
    for city in sorted(cities, key=len, reverse=True):
        if city in combined_text and city not in reverse:
            code = generate_hash_code(city, "CITY", salt)
            mapping[code] = city
            reverse[city] = code

    # 處理人名與 ID (合併處理以 REV 為前綴)
    for per in sorted(persons, key=len, reverse=True):
        if per in combined_text and per not in reverse:
            prefix = "PROJECT" if any(re.match(p, per) for p in PROJECT_ID_PATTERNS) else "REV"
            code = generate_hash_code(per, prefix, salt)
            mapping[code] = per
            reverse[per] = code

    # 處理機構關鍵字偵測
    # 若文字中包含某關鍵字且長度適中，視為潛在機構
    for kw in DEFAULT_ORG_KEYWORDS:
        # 簡單模式：匹配 關鍵字 前後的 2-10 個字
        pattern = r"[\u4e00-\u9fa5]{2,10}" + re.escape(kw)
        matches = re.findall(pattern, combined_text)
        for m in matches:
            if m not in reverse:
                code = generate_hash_code(m, "ORG", salt)
                mapping[code] = m
                reverse[m] = code

    return mapping, reverse


def sanitize_text(text: str, reverse_mapping: dict) -> str:
    """執行文字替換與正則清洗"""
    if not isinstance(text, str):
        return text
    
    # 替換對照表中的實體 (由長到短避免衝突)
    for real_name in sorted(reverse_mapping.keys(), key=len, reverse=True):
        # 確保 real_name 不是已經替換過的代碼格式
        if not (real_name.startswith('[') and real_name.endswith(']')):
            text = text.replace(real_name, reverse_mapping[real_name])
            
    # 正則清洗個資
    for pattern, replacement in REGEX_RULES:
        text = re.sub(pattern, replacement, text)
        
    return text


def save_mapping_with_backup(mapping: dict, reverse: dict, output_dir: str):
    """儲存對照表主檔與備份"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    backup_dir = output_path / "mapping_backups"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_data = {
        "_metadata": {
            "version": "2.1",
            "created_at": timestamp,
            "total_entities": len(mapping),
        },
        "code_to_real": mapping,
        "real_to_code": reverse,
    }

    main_path = output_path / "mapping_dict.json"
    backup_path = backup_dir / f"mapping_dict_{timestamp}.json"

    for path in [main_path, backup_path]:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)

    print(f"  [OK] 對照表已定稿：{main_path} (共 {len(mapping)} 筆)")
    return str(main_path)


# ──────────────────────────────────────────────
# 區塊三：檔案 IO 處理
# ──────────────────────────────────────────────

def process_file(input_path: str, output_path: str, reverse_mapping: dict):
    """根據擴展名處理不同的檔案類型"""
    ext = Path(input_path).suffix.lower()
    
    if ext in [".xlsx", ".xls"]:
        df_dict = pd.read_excel(input_path, sheet_name=None)
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet, df in df_dict.items():
                df.applymap(lambda x: sanitize_text(str(x), reverse_mapping) if pd.notna(x) else x).to_excel(writer, sheet_name=sheet, index=False)
        print(f"  [OK] Excel 已處理：{output_path}")
        
    elif ext == ".csv":
        df = pd.read_csv(input_path, encoding="utf-8-sig")
        df.applymap(lambda x: sanitize_text(str(x), reverse_mapping) if pd.notna(x) else x).to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"  [OK] CSV 已處理：{output_path}")
        
    elif ext in [".txt", ".md"]:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sanitize_text(content, reverse_mapping))
        print(f"  [OK] 文字檔已處理：{output_path}")


def collect_texts(input_path: str) -> list[str]:
    """收集輸入檔中的所有文字內容"""
    ext = Path(input_path).suffix.lower()
    texts = []
    try:
        if ext in [".xlsx", ".xls"]:
            df_dict = pd.read_excel(input_path, sheet_name=None)
            for df in df_dict.values():
                texts.extend(df.astype(str).values.flatten().tolist())
        elif ext == ".csv":
            df = pd.read_csv(input_path, encoding="utf-8-sig")
            texts.extend(df.astype(str).values.flatten().tolist())
        elif ext in [".txt", ".md"]:
            with open(input_path, "r", encoding="utf-8") as f:
                texts.append(f.read())
    except Exception as e:
        print(f"  [WARN] 讀取時發生錯誤: {e}")
    return texts


# ──────────────────────────────────────────────
# 區塊四：主程式
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="資料去識別化工具 V2.1")
    parser.add_argument("--input", required=True, help="禁區輸入檔案路徑")
    parser.add_argument("--output", default="C:\Users\user\Project_Hub\02_去識別化數據", help="AI 工作區輸出路徑")
    parser.add_argument("--mapping-dir", default="c:\Users\user\.gemini\antigravity\brain\My_AI_Project\confidential", help="對照表儲存目錄 (禁區)")
    parser.add_argument("--custom-entities", default="", help="自訂詞庫 (選填)")
    parser.add_argument("--salt", default="ANTIGRAVITY_SECURE_2026", help="雜湊鹽值")

    args = parser.parse_args()

    print("\n" + "=" * 50)
    print("  Sanitizer V2.1 - 去識別化強化版啟動")
    print("=" * 50)

    # 步驟 1: 掃描
    texts = collect_texts(args.input)
    
    # 步驟 2: 建立 Mapping
    # 載入自訂詞庫 (如果有)
    custom = {}
    if args.custom_entities and os.path.exists(args.custom_entities):
        with open(args.custom_entities, "r", encoding="utf-8") as f:
            custom = json.load(f)
            
    mapping, reverse = build_mapping(texts, custom, args.salt)
    
    # 步驟 3: 存檔
    save_mapping_with_backup(mapping, reverse, args.mapping_dir)
    
    # 步驟 4: 執行清洗
    process_file(args.input, args.output, reverse)

    print("\n" + "=" * 50)
    print("  [OK] 任務完成。")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()



