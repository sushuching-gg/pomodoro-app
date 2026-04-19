---
name: phantom-plan-reviewer
description: 計畫書審查助手 - 專門用於校對計畫書中的 工作項目 與 KPI 邏輯是否一致。
---

# 👨‍🏫 計畫書審查助手 (Plan Reviewer)

## 📌 核心定位
本工具用於「計畫輔導」與「修正副本」階段，協助 PO 快速識別縣市計畫書內部的邏輯斷點。

## 🛠️ 主要功能
1. **邏輯校對 (Logic Check)**: 自動比對「工作項目」與「KPI 指標」是否成對出現。
2. **內容提取**: 快速抓出計畫名稱、預算總額與核心任務摘要。

## 📖 使用說明
```bash
python skills/phantom-plan-reviewer/scripts/plan_reviewer.py --input "計畫書檔案路徑.docx"
```
