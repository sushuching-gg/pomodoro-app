---
name: phantom-policy-strategist
description: Analyzes policy documents and past performance reports to assist in drafting annual project plans.
---

# Phantom Policy Strategist

This skill helps the Project Office (PO) by extracting key themes from policy documents and summarizing past execution performance.

## Usage

### 1. Analyze Plan and Report

Run the `strategist.py` script with paths to your Plan (.docx) and Report (.xlsx).

```bash
python scripts/strategist.py --plan "plan.docx" --report "report.xlsx" --output "analysis.txt"
```

### Options

- `--plan`: Path to the Word document containing the policy plan (e.g., "115年度推動運動科技場域實證計畫...docx").
- `--report`: Path to the Excel file containing the execution report (e.g., "專辦月報.xlsx").
- `--output`: (Optional) Path to save the analysis report (e.g., "analysis.txt"). Recommended to avoid console encoding issues.

## Output

The script generates a summary in **Traditional Chinese (繁體中文)**:
- **計畫書分析摘要 (Plan Analysis)**: Extracted sections like "計畫目標" and "工作項目".
- **執行報告分析摘要 (Report Analysis)**: A preview of the execution data from the Excel report.
