import os
from datetime import datetime
from collections import Counter

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        self.log_path = config['knowledge_base']['output_log_path']
        self.report_output_path = os.path.join("output", f"weekly_report_{datetime.now().strftime('%Y%m%d')}.md")

    def generate_report(self):
        print(f"正在生成週報... 來源: {self.log_path}")
        logs = self._parse_log_file()
        
        if not logs:
            print("無日誌資料可生成報告。")
            return

        report_content = []
        report_content.append(f"# 運動實證計畫 - 週報 Summary ({datetime.now().strftime('%Y/%m/%d')})\n")
        
        # 1. 本週足跡 (進度對比)
        report_content.append("## 1. 本週足跡 (Footprint)\n")
        report_content.append(self._generate_stats_chart(logs))
        
        # 2. 紅字事件 (Red Flags)
        report_content.append("## 2. 紅字事件 (Red Flags)\n")
        red_flags = [l for l in logs if "待處理" in l['status'] or "處理中" in l['status'] or "[待核准草稿]" in l['note']]
        if red_flags:
            for item in red_flags:
                report_content.append(f"- **[{item['location']}]** {item['description']} (狀態: {item['status']})")
                if item['note']:
                    report_content.append(f"  - *備註: {item['note'].strip()}*")
        else:
            report_content.append("- 本週無重大未解異常。")
        report_content.append("\n")

        # 3. 下週導航 (Navigation)
        report_content.append("## 3. 下週導航 (Next Week Navigation)\n")
        if red_flags:
            report_content.append(f"- **優先處理**: 共有 {len(red_flags)} 件異常需追蹤。")
            report_content.append("- **建議行動**: 請經理審核「待核准」項目，並確認「處理中」案件的廠商進度。")
        else:
            report_content.append("- **常規執行**: 維持目前SOP運作，建議下週重點轉向數據品質抽查。")

        # Write to file
        with open(self.report_output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        
        print(f"週報已生成: {self.report_output_path}")
        return self.report_output_path

    def _parse_log_file(self):
        if not os.path.exists(self.log_path):
            return []
        
        logs = []
        with open(self.log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header key lines
        for line in lines:
            if "|" not in line or "---" in line or "時間" in line:
                continue
            
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6: # Empty string at start and end due to split
                logs.append({
                    "time": parts[1],
                    "location": parts[2],
                    "status": parts[3],
                    "description": parts[4],
                    "note": parts[5]
                })
        return logs

    def _generate_stats_chart(self, logs):
        locations = [l['location'] for l in logs]
        loc_counts = Counter(locations)
        
        chart_lines = ["各場域事件量統計："]
        for loc, count in loc_counts.items():
            bar = "█" * count
            chart_lines.append(f"- {loc}: {bar} ({count})")
            
        return "\n".join(chart_lines) + "\n"
