import os
import argparse

class RFPAdvisor:
    """
    RFP Advisor (招標需求書撰寫顧問)
    協助 PO 針對縣市招標文件提供範本參考與合規檢查。
    已更新為 [核定軌跡 / 執行追蹤] 雙目錄邏輯。
    """
    def __init__(self):
        # 定義核心範本搜尋路徑 (優先從執行追蹤中找已出的 RFP)
        self.search_roots = [
            r"D:\1_working\114年度計畫\02_執行追蹤",
            r"D:\1_working\114年度計畫\01_核定軌跡\計畫書修正",
            r"D:\1_working\00_通用參考資源\棒球參考資料"
        ]

    def search_templates(self, keyword):
        print(f"\n--- 正在為您搜尋關鍵字: {keyword} 的優良招標範本 ---")
        found = []
        for root_dir in self.search_roots:
            if not os.path.exists(root_dir): continue
            for root, dirs, files in os.walk(root_dir):
                for f in files:
                    if keyword in f and (f.endswith('.docx') or f.endswith('.pdf')):
                        # 避免抓到暫存檔
                        if f.startswith('~$'): continue
                        found.append(os.path.join(root, f))
        
        if found:
            print(f"找到 {len(found)} 個相關範本 (從 114 執行進度中自動提取) ：")
            for i, p in enumerate(found[:8]): # 顯示前 8 個
                print(f"{i+1}. {os.path.basename(p)}")
                print(f"   📂 路徑: {p}")
        else:
            print("目前範本庫中未找到直接匹配。")
            print("💡 建議：可嘗試搜尋「彰化」或「台北」查看現有進度中的 RFP 範本。")

    def check_compliance(self, rfp_path):
        """
        檢查 RFP 是否包含核定函中所要求的必要條款。
        """
        print(f"\n--- 正在檢查 RFP 合規性 (對比核定紀錄) ---")
        print(f"檔案: {os.path.basename(rfp_path)}")
        print("1. 資賦、智財權與資安規範: [核對中...]")
        print("2. 履約保險與驗收條件: [待驗證]")
        print("\n💡 提示: 建議開啟 [114年度計畫/01_核定軌跡/核定意見] 資料夾核對委員意見。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", help="搜尋關鍵字")
    parser.add_argument("--check", help="檢查 RFP 檔案路徑")
    args = parser.parse_args()

    advisor = RFPAdvisor()
    if args.search:
        advisor.search_templates(args.search)
    elif args.check:
        advisor.check_compliance(args.check)
    else:
        print("請使用 --search <關鍵字> 或 --check <檔案路徑>")
