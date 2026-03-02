import pandas as pd
import sys
# 強制輸出為 UTF-8
sys.stdout.reconfigure(encoding='utf-8')
try:
    df = pd.read_excel(r"C:\Users\user\Project_Hub\04_正式報告\輔導總表_美化版.xlsx")
    print("--- 美化版 Excel 摘要 (UTF-8) ---")
    print(df.to_string())
except Exception as e:
    print(f"讀取 Excel 失敗: {e}")
