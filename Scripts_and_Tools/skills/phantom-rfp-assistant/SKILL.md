---
name: phantom-rfp-assistant
description: 招標需求書撰寫顧問 (RFP Advisor) - 協助搜尋歷史優良範本並檢查合規性。
---

# 📝 招標需求書撰寫顧問 (RFP Advisor)

## 📌 核心定位
定位於 **「計畫中期」 (Q1 期初輔導階段)**，協助縣市承辦人從資料夾中找出最相關的範例進行撰寫參考。

## 🛠️ 主要功能
1. **範本檢索 (Smart Search)**: 從 `D:\1_working` 範本庫中搜尋類似計畫的優秀 RFP。
2. **合規引導**: 提醒縣市植入資安、智財、保險等中央必備條款。

## 📖 使用說明
```bash
# 搜尋範本
python skills/phantom-rfp-assistant/scripts/rfp_advisor.py --search "租借系統"

# 檢查合規性
python skills/phantom-rfp-assistant/scripts/rfp_advisor.py --check "縣市RFP草案.docx"
```
