import json
import collections
import os
import sys

def analyze():
    # Load all data
    items = []
    
    # 1. Batch Report
    try:
        if os.path.exists('batch_scan_report.json'):
            with open('batch_scan_report.json', 'r', encoding='utf-8') as f:
                d = json.load(f)
                items.extend(d.get('success_data', []))
    except: pass
    
    # 2. PDF Report
    try:
        if os.path.exists('pdf_scan_results.json'):
            with open('pdf_scan_results.json', 'r', encoding='utf-8') as f:
                pd = json.load(f)
                items.extend([i for i in pd if 'error' not in i])
    except: pass

    # Categories
    cats = {
        'Plan/Call': ['申請', '須知', '說明會', '徵件', '招標', '規範'],
        'Review': ['審查', '意見', '回覆', '修正', '核定', '評選', '初審', '複審'],
        'Execute': ['輔導', '訪視', '座談會', '工作坊', '期中', '進度', '查核', '月報', '季報', '共識營'],
        'Close': ['期末', '成果', '結案', '驗收', '核銷', '決算'],
        'Admin': ['簽到', '會議記錄', '議程', '函', '簽', '開會通知', '名單', '通訊錄']
    }

    stats = collections.defaultdict(lambda: collections.Counter())
    timeline = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

    print(f'Analyzing {len(items)} documents...')

    for item in items:
        meta = item.get('metadata', {})
        y = meta.get('year', 'Unknown')
        m = meta.get('month', 'Unknown')
        
        text = (item.get('filename', '') + ' ' + item.get('content_summary', '')).lower()
        
        matched_any = False
        for cname, kws in cats.items():
            if any(k in text for k in kws):
                stats[y][cname] += 1
                if m != 'Unknown':
                    timeline[y][cname][m] += 1
                matched_any = True
        
        if not matched_any:
            stats[y]['Other'] += 1

    # Report
    years = sorted([x for x in stats.keys() if x != 'Unknown'], key=lambda x: int(x) if x.isdigit() else 999)
    if 'Unknown' in stats: years.append('Unknown')

    for y in years:
        total = sum(stats[y].values())
        print(f'\n--- Year {y} (Total processed: {total}) ---')
        # Print in logical order
        logical_order = ['Plan/Call', 'Review', 'Execute', 'Close', 'Admin', 'Other']
        for c in logical_order:
            count = stats[y][c]
            if count > 0:
                print(f'{c}: {count} ({count/total*100:.1f}%)')
                # Peak month
                peak = timeline[y][c].most_common(1)
                if peak:
                     print(f'  Peak Month: {peak[0][0]} ({peak[0][1]} docs)')

if __name__ == '__main__':
    analyze()
