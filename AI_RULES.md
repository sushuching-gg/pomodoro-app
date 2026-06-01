# 專案開發元守則 (Project Meta-Rules)

## 1. 指令持久性原則 (Instruction Persistence)
- 當使用者在指令中明確要求「保留好的部分」時，這些功能/設計即進入「鎖定狀態」。
- 後續任何修正、優化、重構，均不得以任何理由移除或削弱這些鎖定功能。

## 2. 局部修正不擴大化 (Localized Fix)
- 修正特定問題（如排版、閃光）時，必須確保非相關功能的程式碼（如計時邏輯、五官表情）不被意外更改。

## 3. 變更前之回溯檢查 (Pre-change Backtrack)
- 每次產出新代碼前，必須主動比對前序成功的里程碑，確保新版本是舊版本的「功能加總」，而非「功能替換」。

## 4. 網頁開發編碼規範 (Encoding Standard)
- 所有 HTML 內容必須強制使用 UTF-8 (No BOM) 編碼，特別是包含繁體中文 (開始專注、暫停) 的 UI 元件。
- 每次使用 PowerShell 修改檔案後，必須校對中文字元是否因 System.Text.ASCIIEncoding 噴掉。

## 5. Web Audio 穩定性準則 (Audio Policy)
- 基於瀏覽器 Autoplay 規範，所有音訊初始化 (AudioContext) 必須綁定在使用者點擊事件 (onclick) 內。
- 關鍵提醒 (最後 5 秒) 應確保 AudioContext.state 為 running，必要時自動執行 resume()。
