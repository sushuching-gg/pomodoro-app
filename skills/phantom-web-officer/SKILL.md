---
name: phantom-web-officer
description: 專案辦公室智慧助手，提供計畫輔導、執行監控與效益驗證。
---

# Phantom Web Officer（專案辦公室助手）

此 Skill 協助專案辦公室管理多場域計畫的計畫輔導、執行監控與效益驗證。

---

## 功能

### 1. 計畫輔導 (Plan Coach)
分析計畫書草稿，提供架構與內容建議。
`ash
python skills/phantom-web-officer/scripts/plan_coach.py \
  --draft "draft.docx" \
  --type "sports_tech"
`

### 2. 執行監控 (Execution Monitor)
根據進度報告追蹤里程碑達成情況。
`ash
python skills/phantom-web-officer/scripts/execution_monitor.py \
  --report "progress.xlsx"
`

### 3. 效益驗證 (Benefit Evaluator)
評估 KPI 達成率與質化效益。
`ash
python skills/phantom-web-officer/scripts/benefit_evaluator.py \
  --data "final_data.csv"
`

---

## 架構規範（2026-02 更新）

### ✅ 觸發條件設定位置
此 Skill 的觸發 regex pattern **必須定義在 config/agent_config.yaml 的 skill_triggers 區塊**，
不得硬編碼於 dvisor.py 或任何 Python 原始碼中。

範例（agent_config.yaml）：
`yaml
skill_triggers:
  - pattern: "(計畫書|Draft).*(檢查|分析)|(檢查|分析).*(計畫書|Draft)"
    skill: "phantom-web-officer"
    script: "plan_coach"
    default_args: ["--type", "sports_tech"]
`

### ✅ 測試檔案路徑規範
**禁止**在任何 Python 原始碼中硬編碼測試用的本機路徑（如 D:\1_working\...）。
測試路徑一律從 CLI 傳入：
`ash
python phantom-cassini/src/main.py --draft "D:\path\to\draft.docx"
`

### ✅ 輸出規範
- 所有輸出改用 logging 模組（非 print()），支援 log level 控制
- 輸出語言：**繁體中文**

### ✅ 腳本設計原則
- 支援 rgparse CLI 參數，避免寫死任何路徑或設定值
- 每個腳本視為獨立執行單元（可由 SkillManager 呼叫，也可直接執行）
- 新增腳本後，SkillManager 會自動發現（不需更改 skill_manager.py）
