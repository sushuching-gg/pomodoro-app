# Phantom Manager Deployment Guide (部署手冊)

本手冊將指導您將本地模擬的「影子經理」架構部署至 Google Vertex AI Agent (或同級 Agent 平台)。

## Phase 1: Agent 「大腦」設定 (Prompt Engineering)
我們將 `agent_config.yaml` 轉換為 LLM 可理解的 System Prompt。

- **操作**：在 Agent Console 的 "Instructions" 或 "System Prompt" 欄位貼上 `deployment_assets/system_prompt.txt` 的內容。
- **重點**：Prompt 已包含 Persona、核心指令 (資料攔截、語義糾錯) 與決策邊界 (Guardrails)。

## Phase 2: 知識庫掛載 (Knowledge Base)
讓 Agent 讀懂 SOP。

- **操作**：
    1. 前往 Agent Console 的 "Data Stores" 或 "Knowledge" 區塊。
    2. 建立新 Datastore，選擇 "Cloud Storage" 或 "Google Drive" 作為源。
    3. 上傳我們準備好的 `knowledge_base/sop_manual.md` (或轉換為 PDF)。
    4. 設定同步頻率為「每日」。

## Phase 3: 「手腳」串接 (Tools / Function Calling)
賦予 Agent 寫入日誌與生成報表的能力。

我們需要定義兩個主要工具：
1. `append_project_log`: 用於寫入結構化日誌。
2. `generate_weekly_report`: 用於觸發週報生成。

- **操作**：
    1. 在 Agent Console 的 "Tools" 區塊，選擇 "Create Tool"。
    2. 選擇 "OpenAPI" 或 "Function Declaration"。
    3. 複製 `deployment_assets/tools_schema.json` 中的定義貼上。
    4. **Backend 實作**：
        - 若使用 Vertex AI Agent Builder，這些工具通常對接 **Cloud Functions**。
        - 需將 `src/log_manager.py` 與 `src/report_generator.py` 的邏輯封裝為 HTTP Cloud Functions。

## Phase 4: 測試與驗收 (Validation)
1. **單元測試**：在 Console 測試視窗輸入：「大安場域 10:00 設備運作正常」。
2. **檢查點**：確認系統是否回覆「已記錄」，並查看 Log (或 Sheet) 是否新增該筆資料。
3. **邊界測試**：輸入「要求退費」，確認是否觸發「待核准」標籤。
