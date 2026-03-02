# My_AI_Project - Phantom Manager 專案總覽

## 專案定位
本專案使用 AI 代理人技術，輔助「推動運動科技場域實證計畫」(111-115年) 的日常業務執行。
所有 AI 工具皆圍繞同一個核心任務：**讓計畫管理工作更高效。**

---

## 目錄結構與業務對應

`
My_AI_Project/
|
+-- phantom-cassini/          # 核心大腦 (AI Agent 主程式)
|   +-- src/                  #    意圖識別、技能調度、主流程
|   +-- scripts/              #    批量處理工具 (batch_processor.py)
|
+-- phantom-rfp-assistant/    # RFP 輔助 (招標/服務建議書)
|   +-- scripts/              #    對應業務: 115部內招標文件, 縣市招標需求書
|
+-- skills/                   # 技能模組庫
|   |
|   |  -- 業務核心技能 --
|   +-- phantom-web-officer/  # 計畫書管理 (解析/檢核/評分)
|   |   +-- scripts/          #    plan_parser.py, plan_coach.py
|   |                         #    對應業務: 114計畫核定, 計畫書修正, 歷史資料存檔
|   |
|   +-- phantom-file-navigator/ # 檔案導航 (快速搜尋定位)
|   |                         #    對應業務: 全部業務資料夾的快速檢索
|   |
|   +-- phantom-policy-strategist/ # 政策分析 (待開發)
|   |                         #    對應業務: 運科跨部會報告, 114參考資料
|   |
|   +-- phantom-manager/      #    Phantom 人設與指令定義
|   |
|   |  -- 通用工具技能 --
|   +-- ppt-generator/        # Markdown to PPT 轉換
|   +-- youtube_summarizer/   # YouTube 影片摘要
|   +-- anthropics_skills/    #    範例技能庫 (參考用)
|
+-- sue_life_work_log/        # 生活工作日誌 (Flask Web App)
|
+-- README.md                 # 本文件
`

---

## AI 工具 vs 實際業務 對照表

| AI 工具 | 用途 | 對應的業務資料 (D:\1_working) |
|---------|------|------------------------------|
| phantom-cassini | 核心大腦，調度所有技能 | (全域) |
| phantom-web-officer | 計畫書解析、合規檢核、自動評分 | 114計畫核定/計畫書修正、3_資料存檔 |
| phantom-file-navigator | 在大量檔案中快速搜尋 | D:\1_working 全域 |
| phantom-rfp-assistant | 招標文件與服務建議書輔助 | 1_115新年度規劃/1_115部內招標文件 |
| phantom-policy-strategist | 政策與跨部會資料分析 | 運科跨部會報告、會議資料 |
| ppt-generator | 快速製作簡報 | 113年構想簡報、各類報告 |

---

## 業務資料目錄 (D:\1_working)

`
D:\1_working/
+-- 114計畫核定/          # 6 縣市核定計畫書 (AI 已完成全量掃描)
+-- 2_114計畫執行/        # 月報、招標需求書、資安政策
+-- 1_115新年度規劃/      # 115年專辦計畫書、經費規劃、招標文件
+-- 3_資料存檔/           # 111-114年歷史資料 (AI 已掃描 1,067 檔)
|   +-- 2023/            #   112年: 期中/期末報告、訪視、結案審查
|   +-- 2024/            #   113年: 構想簡報、計畫書輔導、座談會
|   +-- 2025/            #   114年: 臺北市2.0 等
+-- 彰化114計畫特訓/      # 棒球+走跑 會議記錄與需求書
+-- 會議資料/
+-- 新聞稿/
+-- 棒球參考資料/
+-- 運科跨部會報告/
`

---

## 目前進度 (2026-02-20)

### 已完成
- phantom-cassini 核心系統整合
- phantom-web-officer 計畫書檢核 (實戰就緒)
- phantom-file-navigator 檔案導航
- ppt-generator 簡報產生器
- youtube_summarizer 影片摘要
- 歷史資料首次全量掃描 (89% 成功率)

### 進行中
- 修復批量掃描的 CP950 編碼問題 (114 筆待修)
- 跨年度趨勢報告 (multi_year_trend_report.json)

### 待開發
- execution_monitor (執行進度監控)
- benefit_evaluator (效益評估)
- phantom-policy-strategist 核心腳本
- phantom-rfp-assistant 核心腳本
