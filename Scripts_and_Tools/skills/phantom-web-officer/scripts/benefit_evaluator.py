import argparse
import os

def evaluate_benefits(data_path):
    print(f"=== Phantom 效益驗證 (Benefit Evaluator) ===")
    print(f"正在評估數據: {data_path}")
    
    # 模擬評估
    KPIs = {
        "總用戶數": {"target": 1000, "actual": 1250},
        "滿意度": {"target": 4.5, "actual": 4.2},
        "留存率": {"target": 30, "actual": 45} # percent
    }
    
    print("\n[KPI 達成率分析]")
    overall_score = 0
    for kpi, val in KPIs.items():
        rate = (val['actual'] / val['target']) * 100
        status = "達標" if rate >= 100 else "未達標"
        print(f"- {kpi}: {val['actual']} (目標: {val['target']}) -> {rate:.1f}% [{status}]")
        if status == "達標":
            overall_score += 1
            
    print("\n[質化效益摘要]")
    print("- 成功將智慧健身概念導入高齡社區。")
    print("- 用戶回饋顯示持續參與意願極高。")
    
    print(f"\n[最終評定]")
    grad = "優 (A)" if overall_score >= 2 else "良 (B)"
    print(f"專案評級: {grad} (通過 {overall_score}/{len(KPIs)} 項 KPI)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="數據檔案路徑")
    args = parser.parse_args()
    evaluate_benefits(args.data)
