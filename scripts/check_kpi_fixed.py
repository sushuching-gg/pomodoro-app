import pandas as pd
df = pd.read_excel(r"D:\Project_Hub\03_分析草稿\V3.2.1_KPI_FIXED.xlsx")
kpi_row = df[df['維度'].str.contains('KPI', na=False)]
print(kpi_row[['維度', '狀態', '數據', '建議']].to_string())
