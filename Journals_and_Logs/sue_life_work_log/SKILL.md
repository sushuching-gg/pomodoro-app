# 🛠️ Sue's Life & Work Log: 核心設計規範 (Skill Specification)

## 📍 1. 系統架構 (System Architecture)
- **核心引擎**：基於 Flask 的輕量化 Web Server。
- **資料儲存**：採用 Markdown 搭配 YAML Frontmatter 的「文件即資料庫」模式。
- **緩存機制**：實作基於檔案修改時間 (mtime) 的記憶體快取，降低頻繁讀取造成的 I/O 負擔。

## 🌐 2. 跨裝置連線設計 (Multi-device Connectivity)
- **自動偵測**：系統啟動時透過 socket 自動獲取 Local IP 與 Hostname。
- **終極解決方案 (Tailscale)**：當 Local DNS 不穩定或 IP 頻繁跳動時，強制推行 **Tailscale (Mesh VPN)**。
- **永久網址**：透過 Tailscale 固定專屬 IP (如 100.99.205.25) 實現跨網段、跨區域的永久存取。
- **Session 持久化**：手機存取場景下，PERMANENT_SESSION_LIFETIME 應設為 **7 天**，以解決頻繁鎖屏導致的反覆登入困擾。

## 🔐 3. 安全管理設計 (Security Design)
- **管理員權限**：實作 admin_required 裝飾器，透過 session 管理登入狀態。
- **密碼保護**：系統需具備 /admin/login 表單，校驗密碼 (預設: sue2026)。
- **路徑防護**：檔案讀取必須經過 safe_path 校驗，防止路徑遍歷攻擊。

## 🎬 4. 多媒體處理邏輯 (Media Handling)
- **自動偵測**：上傳檔案時依據後綴名自動分類 (Image/Video/Audio)。
- **嵌入生成**：
    - 圖片：![title](url)
    - 影片：<video controls>...</video>
- **共置路徑**：媒體檔案與對應的 .md 檔案儲存在相同的分類目錄下。

## ⚠️ 5. 維護與穩定性關鍵節點 (Stability & Maintenance)
- **【最高準則：網路修復】**：若手機無法連線，優先執行 ix_network.bat 自動修復防火牆規則 (需管理員權限)。
- **【重啟機制】**：變更 app.py 後必須重啟 estart_server.bat。
- **【亂碼防護】**：Windows 下編輯 Batch 檔案必須確保編碼為 UTF-8 (無 BOM) 以免指令失效。
- **日誌追蹤**：維持 server.log 寫入。

## 📂 6. 目錄分類規範 (Category Mapping)
- work: 工作項目。
- life/travel: 旅遊紀錄。
- life/daily/me: 個人生活。
- life/daily/grandma: 阿嬤生活。
- videos: 影片專案。