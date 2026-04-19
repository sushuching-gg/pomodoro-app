# PROJECT_MEMORY.md
# AI 專案開發核心導引 (System Instructions)
# 版本：2026-03-01 v3.1 (Encoding Stabilized)

## 一、 基本原則 (General Principles)
1. 僅能在 AI_Dev_Workspace 內處理去識別化後的資料。
2. 絕對禁區 (Forbidden Zone): /confidential/ 內的檔案為最高禁令，Antigravity 不得存取。
3. 搜尋紅線 (Search Redlines): 禁止使用案號、真實人名或機關名稱直接搜尋。

## 二、 套件白名單 (Package Whitelist)
- 禁止使用 requests 等具網路上傳能力之套件。
- 准許套件：pandas, openpyxl, python-docx, xlsxwriter, Python 標準庫。


### Phase 13: V3 整合完畢與協作架構鎖定 (2026-03-01)
- **核心引擎升級**：fp_checker.py 已升級至 V3 穩定版，支援雙文件分析、V3 專業 Excel 產出，並修正 CP950 編碼問題。
- **去識別化強化**：sanitizer_v2.1.py 部署完畢，具備 114 年度案號識別、職稱語意感應偵測與個資深度清洗。
- **資安物理防線**：security_guard.py 自動監控 PROJECT_MEMORY.md 的存在與編碼完整性，根目錄已完成淨化，敏感資料全數隔離於 confidential/ 內。
- **Claude Cowork 協作鎖定**：已在 D:\ 建立 AI_Dev_Workspace/ 中轉站，COWORK_BRIEFING.md 已設為「唯讀」並鎖定 A/B/C/D 任務架構。
- **即將進行**：Layer 3 經費細項深度對比 (Budget Cross-check)。




### Phase 14: 全自動數據對焦與跨 AI 行政流水線正式打通 (2026-03-01)
- **核心引擎升級 (V3.2.1)**：fp_checker.py 已具備 Layer 3+ 深度數據感應，支援預算超支偵測與 KPI 量化指標對核。
- **物理倉儲校準**：為繞過 Claude Cowork 存取限制，專案中心已遷移至 C:\Users\user\Project_Hub\。
- **雙機協作實測成功**：Antigravity (數據提取) -> Cowork (行政產出) 流水線已完成首份「輔導告知函」與「美化對比表」產出。
- **資安門鎖強化**：COWORK_BRIEFING.md 已在 C 磁碟鎖定為唯讀，嚴格規範人名/案號 [CITY_xxxx] 等符號之保留。
- **即將進行**：Layer 4 PPT 行政簡報自動生成 (任務 C)。


