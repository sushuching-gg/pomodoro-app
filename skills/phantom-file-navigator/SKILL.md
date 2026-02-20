---
name: phantom-file-navigator
description: 智能檔案導航。當使用者需要尋找、查詢或開啟專案檔案時使用。例如：「幫我找上週的報告」、「搜尋關於設備故障的紀錄」、「打開 115年計畫書」。
---

# Phantom File Navigator (智能檔案導航)

這個 Skill 協助使用者在龐大的專案目錄 (D:\1_working) 中快速定位檔案。

## 功能
1.  **建立索引 (Index)**: 掃描整個工作目錄，記錄檔案位置。
2.  **搜尋 (Search)**: 支援模糊關鍵字搜尋。
3.  **開啟 (Open)**: 直接開啟檔案。

## 使用指引

### 1. 搜尋檔案
當使用者詢問檔案位置或搜尋特定關鍵字時：

1.  執行搜尋腳本：
    `ash
    python skills/phantom-file-navigator/scripts/navigator.py search <關鍵字1> <關鍵字2> ...
    `
    例如：python skills/phantom-file-navigator/scripts/navigator.py search 115年 計畫書

2.  解讀回傳的列表，向使用者回報找到的檔案 (包含路徑與最後修改時間)。

### 2. 開啟檔案
當使用者要求「打開」某個檔案，且你已經透過搜尋確定了路徑：

1.  執行開啟腳本：
    `ash
    python skills/phantom-file-navigator/scripts/opener.py <檔案完整路徑>
    `

### 3. 更新索引
若使用者表示找不到最近新增的檔案，或明確要求「更新索引」：

1.  執行索引腳本：
    `ash
    python skills/phantom-file-navigator/scripts/indexer.py
    `

## 限制
- 僅支援 D:\1_working 目錄及其子目錄。
- 索引檔儲存於 skills/phantom-file-navigator/scripts/file_index.json。
