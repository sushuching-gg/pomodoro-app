import argparse
import os
import random

def monitor_execution(report_path):
    print(f"=== Phantom 執行監控 (Execution Monitor) ===")
    print(f"正在監控進度報告: {report_path}")
    
    # 模擬載入資料
    sites = ["基隆", "台北", "新北", "桃園", "台中"]
    
    print("\n[進度儀表板]")
    print("| 場域       | 狀態   | 進度     | 風險等級   |")
    print("|------------|--------|----------|------------|")
    
    for site in sites:
        progress = random.randint(30, 100)
        status = "正常"
        risk = "低"
        
        if progress < 50:
            status = "延遲"
            risk = "高"
        elif progress < 80:
            status = "有風險"
            risk = "中"
            
        print(f"| {site:<10} | {status:<6} | {progress}%      | {risk:<10} |")

    print("\n[預警通知]")
    print("- 基隆場域 回報設備延遲 (2 週)。")
    print("- 台中場域 用戶參與度低於 KPI 目標。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="進度報告路徑")
    args = parser.parse_args()
    monitor_execution(args.report)
