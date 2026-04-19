# Skill: Project Hub Management & Security Guard
## Description: 專案中心化檔案管理與資安監控工具

### 核心功能 (Core Features)
1. **物理中心化管理 (Project_Hub)**：統一管理標案資料流 (01 原始 -> 02 去識別 -> 03 分析 -> 04 產出)。
2. **跨 AI 沙盒隔離 (Sandbox Bridge)**：將工作重心遷移至 `C:\Users\user\Project_Hub`，確保 Claude Cowork 存取權限。
3. **桌面歸檔 (Desktop Cleanup)**：提供 `cleanup_desktop.py` 腳本，一鍵清理桌面並歸檔至專案中心。
4. **全域資安監控 (Security Guard)**：`security_guard.py` 監控 `PROJECT_MEMORY.md` 完整性。

### 核心路徑 (C 磁碟版本)
- **根目錄**: `C:\Users\user\Project_Hub\`
- **監控對象**: `PROJECT_MEMORY.md`, `AI_RULES.md`

### 執行命令 (Execution)
- **同步桌面**: `python cleanup_desktop.py`
- **自檢規範**: `python scripts/security_guard.py`

---
*Last Updated: 2026-03-01 v1.2*
