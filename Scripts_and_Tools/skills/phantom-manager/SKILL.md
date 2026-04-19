---
name: phantom-manager
description: Phantom Manager CLI，用於記錄事件與生成週報。
---

# Phantom Manager (影子經理)

此 Skill 提供 Phantom Manager Agent 的命令列介面，允許使用者記錄事件與生成週報。

## 使用方式

### 1. 記錄事件 (Log)

將新事件寫入每日日誌。Agent 會分析事件內容，並附加必要的標籤或建議。

```bash
python phantom-cassini/scripts/manager_cli.py log "10:30 大安場域 現場設備運作正常"
```

### 2. 生成週報 (Report)

根據日誌內容生成 Markdown 格式的週報。

```bash
python phantom-cassini/scripts/manager_cli.py report
```

## 設定

Agent 設定檔位於 `phantom-cassini/config/agent_config.yaml`。
