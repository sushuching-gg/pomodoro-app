---
name: phantom-po-office
description: 專案辦公室智慧助手，提供計畫輔導、執行監控與效益驗證。
---

# Phantom Project Office (專案辦公室)

此 Skill 協助專案辦公室管理多場域計畫。

## 功能

### 1. 計畫輔導 (Plan Coach)
分析計畫書草稿，提供架構與內容建議。
```bash
python skills/phantom-web-officer/scripts/plan_coach.py --draft "draft.docx" --type "sports_tech"
```

### 2. 執行監控 (Execution Monitor)
根據日誌或里程碑報告追蹤專案進度。
```bash
python skills/phantom-web-officer/scripts/execution_monitor.py --report "progress.xlsx"
```

### 3. 效益驗證 (Benefit Evaluator)
評估 KPI 達成率與質化效益。
```bash
python skills/phantom-web-officer/scripts/benefit_evaluator.py --data "final_data.csv"
```
