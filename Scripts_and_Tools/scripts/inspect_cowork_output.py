import pandas as pd
try:
    df = pd.read_excel(r"C:\Users\user\Project_Hub\04_正式報告\輔導總表_美化版.xlsx")
    print("--- 美化版 Excel 摘要 ---")
    print(df.head(10).to_string())
except Exception as e:
    print(f"讀取 Excel 失敗: {e}")
