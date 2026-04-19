# 🧠 Project Memory - Sue Life Work Log

## 📍 專案基本資訊
- **名稱：** Sue Life Work Log
- **核心目標：** 透過 Web 介面實現個人工作與生活日誌的高效管理。

## 📅 2026-02-23 重要演進與問題解決

### 1. 網路連線革命 (Connectivity Breakthrough)
- **問題**：手機連線極度不穩定。區域網路 IP 隨路由器分配而跳動，電腦名稱 (mDNS) 在某些網路環境失效。
- **最終方案**：引入 **Tailscale (Mesh VPN)**。
- **成果**：
    - 獲取永久固定 IP：100.99.205.25。
    - 實現跨網路 (4G/5G) 存取，不再依賴同一個 Wi-Fi。
    - 建立 ix_network.bat 自動化處理防火牆通訊埠 5000 的開通（需管理員權限）。

### 2. 使用者體驗優化 (UX Improvements)
- **問題**：手機鎖屏或切換 App 後經常需要重新輸入密碼。
- **方案**：將 PERMANENT_SESSION_LIFETIME 從 30 分鐘延長至 **7 天**。
- **成果**：顯著提升移動端錄入效率。

### 3. Windows 環境穩定性問題
- **問題 A (編碼)**：Batch 指令在 UTF-8 帶 BOM 格式下會出現亂碼，導致啟動失敗。
- **問題 B (權限)**：開通通訊埠需要提升權限。
- **解決方案**：
    - 強制所有啟動腳本與 Python 原始碼使用 **UTF-8 (無 BOM)** 編碼。
    - 在 estart_server.bat 中加入詳細啟動路徑顯示與錯誤提示。

## ⚠️ 核心技術規格 (Technical Specs)
- **永久網址**：http://100.99.205.25:5000
- **安全機制**：全局 efore_request 登入攔截，Session 加密存儲。
- **啟動入口**：estart_server.bat (清理舊程序 -> 顯示網址 -> 啟動 Flask)。

## 🚀 明日測試重點
- 驗證裝置休眠後重啟，Tailscale 是否能自動恢復連線。
- 測試在大規模多媒體上傳時，Session 是否依然穩定。
### 4. 懶人模式：隱藏視窗啟動 (Background Implementation)
- **問題**：使用者關閉 CMD 視窗後網頁斷線。
- **解決方案**：實作背景啟動套件：
    - `run_silently.bat`：無暫停的啟動邏輯。
    - `start_hidden.vbs`：呼叫批次檔並隱藏視窗。
    - `stop_server.bat`：強制終止背景程序的工具。
- **成果**：使用者可一鍵啟動後關閉所有視窗，日誌系統依然在背景穩定服務。

### Phase 8: 系統穩定性強化與啟動標準化 (2026-02-24)
- **環境相容性修正**：解決了 Windows CMD (CP950) 對 UTF-8 批次檔與 Emoji 的相容性問題。將 pp.py 啟動輸出與 START_SUE_LOG.bat 全面改為純英文/ASCII，防止因編碼衝突導致的閃退。
- **簡化啟動流程**：於專案根目錄建立 START_SUE_LOG.bat 作為唯一標準入口，自動處理 Port 5000 被佔用的清理工作。
- **路徑與導航修復**：修正 ase.html 中 href="/life" 的 404 連結，將其指向 /life/travel，並在 pp.py 增加別名路由以確保新舊路徑皆可通。
- **檔案索引更新**：phantom-file-navigator 現已能同時索引 D:\1_working 與當前專案目錄，確保所有 PROJECT_MEMORY.md 皆可被搜尋。
- **維護建議**：保持 CMD 視窗開啟即可維持服務，若欲停止請直接關閉視窗或使用 Ctrl+C。
