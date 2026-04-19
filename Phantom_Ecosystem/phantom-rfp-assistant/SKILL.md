---
name: phantom-rfp-assistant
description: 協助檢核縣市 114年 運動科技場域實證計畫招標文件 (RFP)，確保符合專案辦公室 (PO) 的規範要求。
---

# 🤖 Phantom RFP Assistant

**針對痛點**：
114年 Q1 (3月) 期初輔導期間，需協助縣市擬定高品質的招標文件 (Request for Proposal, RFP)，避免因規格不符導致流標或執行困難。

**核心功能**：
1.  **DOCX 掃描**：讀取縣市上傳的招標文件草案。
2.  **合規性檢核 (Compliance Check)**：
    - **必要條款**：智慧財產權條款、驗收標準、經費編列上限 (如便當費)。
    - **關鍵字偵測**：「運動科技」、「場域實證」、「KPI」。
3.  **風險提示 (Risk Alert)**：標註可能導致流標的高風險條款。

**使用說明**：

1.  準備縣市招標文件 (DOCX 格式)。
2.  執行檢核腳本：
    `ash
    python phantom-rfp-assistant/scripts/rfp_checker.py --input path/to/rfp.docx
    `
3.  檢視生成的 fp_check_report.md 報告。

**依賴資源**：
- esources/compliance_rules.json: 定義 Pass/Fail 的規則清單。
- scripts/rfp_checker.py: 核心檢核邏輯。
