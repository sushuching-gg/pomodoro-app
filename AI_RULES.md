# 📜 My_AI_Project AI 協作開發準則 (Master AI Rules v3)

## 1. 核心開發規範
- **分工架構**：Antigravity 負責維護工具（sanitizer/restorer/rfp_checker），不接觸真實資料；Claude Cowork 執行日常任務。
- **開發前核准 (SOP)**：開始任何工作前，必須列出 1) 功能清單 2) 套件清單 3) 路徑清單，獲核准後方可撰寫。
- **套件白名單**：僅限使用 PROJECT_MEMORY.md 中列出之套件，生成腳本必須包含「套件透明清單」。

## 2. 資安與搜尋紅線
- **搜尋泛化**：禁止使用計畫案號、標案編號直接搜尋。搜尋前必須泛化關鍵字（如「運動科技政府補助細則」）。
- **禁區存取**：非去識別化之原始資料（/confidential/）為絕對禁區，AI 工具嚴禁存取。
- **編碼保護**：寫入文件必須指定 UTF-8，讀取 JSON 統一使用 utf-8-sig。

## 3. 輸出品質標準
- **代碼保留**：去識別化代碼（如 [CITY_xxxx]）必須原封不動保留在輸出報告中。
- **V3 報告格式**：RFP 檢核優先產出 V3 整合版 Excel，包含「Soul/Body/KPI/Suggest」維度。
