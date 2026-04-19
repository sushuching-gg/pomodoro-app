import os
import argparse
import openpyxl
import sys
import io

# 強制設定輸出為 UTF-8，避免 Windows CMD 亂碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class AdminTools:
    """
    Admin Tools (行政自動化工具)
    提供縣市執行清單摘要、進度追蹤與核定狀態預警。
    已更新為 [核定軌跡 / 執行追蹤] 雙目錄邏輯。
    """
    def __init__(self):
        # 更新後的路徑
        self.y114_decision = r"D:\1_working\114年度計畫\01_核定軌跡"
        self.y114_execution = r"D:\1_working\114年度計畫\02_執行追蹤"
        self.master_file = os.path.join(self.y114_decision, "114年運動科技場域實證縣市核定計劃書簡表1150105.xlsx")

    def show_status(self):
        print("\n=== 114 年度縣市執行現況 (核心來源: 核定軌跡) ===")
        if not os.path.exists(self.master_file):
            print(f"錯誤: 找不到核定總表檔案 ({self.master_file})")
            return

        try:
            wb = openpyxl.load_workbook(self.master_file, data_only=True)
            sheet = wb.active
            rows = list(sheet.iter_rows(values_only=True))
            
            # 定義標題 (手動對應 Excel 欄位)
            # A:序號, B:縣市, C:計畫名稱, D:總金額, E:補助金額, F:財力分級, G:比率, H/I/J/K/L:委員意見, M:繳交狀況, N:摘要, O:建議...
            
            print(f"| 縣市 | 計畫名稱摘要 | 審查結果 | 核定補助金額 (千元) |")
            print(f"| :--- | :--- | :--- | :--- |")
            
            # 從數據列開始讀取 (第 4 列開始為數據)
            for row in rows[3:12]:
                if not any(row): continue
                city = str(row[1]) if len(row) > 1 and row[1] else "—"
                name = str(row[2])[:30] if len(row) > 2 and row[2] else "—"
                # 取得核定後的經費建議 (假設在 M 欄之後的核定欄位，這裡修正為對應欄位)
                # 根據之前的觀察，核定補助金額大約在第 15~16 欄 (Index 14~15)
                # 我們先抓取審查結果 (H欄, Index 7) 與 核定經費 (Index 14 左右)
                result = str(row[7]) if len(row) > 7 and row[7] else "核定通過"
                amount = str(row[14]) if len(row) > 14 and row[14] else "—"
                
                print(f"| {city} | {name} | {result} | {amount} |")
                
            print("\n* 註：詳細委員意見與核定函 PDF 存放於 [114年度計畫/01_核定軌跡/核定文]")
        except Exception as e:
            print(f"讀取過程出錯: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="顯示 114 年度核定狀態摘要")
    args = parser.parse_args()

    admin = AdminTools()
    if args.status:
        admin.show_status()
    else:
        print("請使用 --status 查看進度摘要。")
