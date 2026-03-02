# Skill: Phantom RFP Checker V3.2.1
## Description: 標案需求書(RFP)與計畫書(Plan)深度數據對核引擎 (Layer 3+ 穩定版)

### 核心功能 (Core Features)
1. **Layer 3: 預算超支自動感應**：能自動提取 Word 表格中的「預算金額」與「計畫總計」，比對是否超支。
2. **Layer 3.1: KPI 量化指標對檢**：針對「人次、場次、%」等單位，自動提取標案目標與計畫承諾，判斷是否達標。
3. **Layer 3.2: 多維度 Excel 輔導報告**：產出包含「KPI (數據對焦)」與「Insight (輔導建議)」的專業分析表。
4. **V3 穩定引擎**：支援 Windows CP950 編碼，解決亂碼問題，並預設輸出至 `Project_Hub\03`。

### 執行命令 (Execution)
```powershell
python skills/phantom-rfp-checker/scripts/rfp_checker.py --rfp <RFP路徑> --plan <計畫路徑> --rules <規則JSON> --output "C:\Users\user\Project_Hub\03_分析草稿\report.xlsx"
```

### 相關檔案 (Resources)
- **核心引擎**: `scripts/rfp_checker.py` (V3.2.1)
- **114 檢核規約**: `rules/mandatory_sections_114.json`

### 與 Cowork 協作協議
- 產出之 Excel 作為 Claude Cowork 的任務 A(Word)、任務 B(Excel)、任務 C(PPT) 的唯一數據來源。

---
*Last Updated: 2026-03-01 v3.2.1*
