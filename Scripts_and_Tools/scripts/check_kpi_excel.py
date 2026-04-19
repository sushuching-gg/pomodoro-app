import pandas as pd
df = pd.read_excel(r"D:\Project_Hub\03_分析草稿\V3.2_KPI_DEEP_CHECK.xlsx", skiprows=3)
kpi_row = df[df['檢核維度'].str.contains('KPI', na=False)]
print(kpi_row[['檢核維度', '狀態', 'KPI (數據對焦)', 'Insight (輔導建議)']].to_string())
