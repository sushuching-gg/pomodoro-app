import json
import collections

try:
    with open('batch_scan_report.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    with open('batch_scan_report.json', 'r', encoding='cp950', errors='ignore') as f:
        data = json.load(f)

# Hardcoded safe keys
keywords = [
    ('棒球', 'Baseball'), ('籃球', 'Basketball'), ('足球', 'Soccer'),
    ('羽球', 'Badminton'), ('桌球', 'Table Tennis'),
    ('游泳', 'Swimming'), ('自行車', 'Cycling'), ('跑步', 'Running'),
    ('健身', 'Fitness'), ('瑜珈', 'Yoga'),
    ('AI', 'AI'), ('大數據', 'Big Data'), ('IoT', 'IoT'), ('5G', '5G'),
    ('VR', 'VR'), ('AR', 'AR'), ('穿戴式', 'Wearable'),
    ('實證', 'Demonstration'), ('數位轉型', 'Digital Transformation'),
    ('高齡', 'Elderly'), ('訓練', 'Training'), ('平台', 'Platform'),
    ('系統', 'System'), ('APP', 'APP')
]

results = collections.defaultdict(collections.Counter)
target_years = ['112', '113', '114']

print('Analyzing keywords...')
for item in data.get('success_data', []):
    y = item.get('metadata', {}).get('year')
    if y not in target_years: continue
    
    # Try multiple decodings if summary text is garbled
    text = (item.get('filename', '') + ' ' + item.get('content_summary', '')).lower()
    
    for zh, en in keywords:
        if zh.lower() in text or en.lower() in text:
            results[y][zh] += 1

print('--- Keyword Trends (112-114) ---')
report = {}
for y in target_years:
    if y in results:
        print(f'\n[Year {y}] Top 10 Keywords:')
        top10 = results[y].most_common(10)
        report[y] = dict(top10)
        for k, v in top10:
             print(f'  {k}: {v}')

with open('keyword_trend_analysis_final.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print('\nSaved to keyword_trend_analysis_final.json')
