import os
import argparse
from docx import Document

class PlanReviewer:
    """
    計畫書審查助手 (Plan Reviewer)
    專門用於校對計畫書中的 工作項目 與 KPI 邏輯是否一致。
    """
    def __init__(self, docx_path):
        self.path = docx_path
        self.sections = {'tasks': [], 'kpis': []}

    def process(self):
        if not os.path.exists(self.path):
            print(f"錯誤: 找不到檔案 {self.path}")
            return
        
        try:
            doc = Document(self.path)
            curr = None
            for p in doc.paragraphs:
                txt = p.text.strip()
                if not txt: continue
                # 識別標題關鍵字
                if any(k in txt for k in ["工作項目", "實施內容", "主要任務"]): 
                    curr = 'tasks'
                elif any(k in txt for k in ["績效指標", "KPI", "成果指標"]): 
                    curr = 'kpis'
                elif p.style.name.startswith('Heading'): 
                    curr = None
                
                if curr and len(txt) > 5:
                    self.sections[curr].append(txt)

            print(f"\n=== 計畫書審查助手 (Plan Reviewer) ===")
            print(f"檔案路徑: {os.path.basename(self.path)}")
            print(f"[提取結果] 工作項目: {len(self.sections['tasks'])} 條 | 績效指標: {len(self.sections['kpis'])} 條")
            
            # 邏輯一致性檢查
            if len(self.sections['tasks']) > 0 and len(self.sections['kpis']) == 0:
                print("\n[⚠️ 邏輯警示] 偵測到多項工作項目，但完全未發現對應的 KPI 績效指標。")
                print("這在計畫審查中通常是重大缺失，請核對是否漏列或格式識別錯誤。")
            elif len(self.sections['tasks']) > 0:
                print("\n[✓ 結構檢查] 檔案結構基本完整，工作項目與 KPI 皆有對應內容。")
                print("\n[預覽] 前三項提取內容：")
                print("--- 工作項目 ---")
                for t in self.sections['tasks'][:3]: print(f"- {t[:60]}...")
                print("\n--- KPI 指標 ---")
                for k in self.sections['kpis'][:3]: print(f"- {k[:60]}...")
                
        except Exception as e:
            print(f"解析過程發生錯誤: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="計畫書邏輯對比審查工具")
    parser.add_argument('--input', required=True, help='計畫書 Word 文件案路徑')
    args = parser.parse_args()
    PlanReviewer(args.input).process()
