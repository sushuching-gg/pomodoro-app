# Skill: Phantom Sanitizer Toolkit V2.1
## Description: 資料去識別化 (假名化) 去敏感工具提升版 (V2.1)

### 核心功能 (Core Features)
1. **語意感應提取 (Context-aware Persona)**：自動識別職稱如「計畫主持人」、「聯絡人」後的姓名，並轉化為 `[REV_xxxx]`。
2. **114 年度專項識別 (Project ID Mapping)**：自動偵測 `114-NTSU-*` 等年度計畫標籤，轉化為 `[PROJECT_xxxx]`。
3. **個資深度清洗 (PII Redaction)**：包含 10 碼身分證、手機號碼、Email 與電話區碼之正規化遮蔽。
4. **絕對隔離機制 (Isolation Gateway)**：
   - 作為真實資料進入 AI 工作區的唯一門鎖。
   - 產出對照表 (`mapping_dict.json`) 於禁區備份，供 `restorer.py` 後續還原。

### 執行命令 (Execution)
```powershell
python scripts/sanitizer_v2.1.py --input <真實資料路徑> --output <AI工作區路徑> --mapping-dir <禁區路徑>
```

### 相關檔案 (Resources)
- **核心工具**: `scripts/sanitizer_v2.1.py`
- **還原工具**: `restorer.py`

### 資安協議 (Security Protocol)
- **Human-in-the-Loop**: 此腳本由使用者手動執行。
- **Data Gap**: 有效防止真實數據（人名、機關、地區）流向雲端。

---
*Last Updated: 2026-03-01 v2.1*
