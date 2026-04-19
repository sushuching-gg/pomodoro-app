import json
import collections

# Load data
data = {'success_data': []}
try:
    with open('batch_scan_report.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f'Error: {e}')
    exit()

keywords = [
    '棒球', '籃球', '足球', '羽球', '桌球', '網球', '排球', 
    '游泳', '自行車', '跑步', '鐵人三項', '健身', '瑜珈',
    'AI', '人工智慧', '大數據', '物聯網', 'IoT', '5G', 'VR', 'AR', 'MR', 'XR',
    '穿戴式', '智慧手錶', '智慧衣', '感測器',
    '場域', '實證', '數位轉型', '精準運動', '健康促進', '高齡', '銀髮',
    '競技', '訓練', '監測', '分析', '平台', '系統', 'APP'
]

results = collections.defaultdict(collections.Counter)
target_years = ['112', '113', '114']

print('Analyzing keywords...')
for item in data.get('success_data', []):
    y = item.get('metadata', {}).get('year')
    if y not in target_years: continue
    
    text = (item.get('filename', '') + ' ' + item.get('content_summary', '')).lower()
    
    for k in keywords:
        if k.lower() in text:
            results[y][k] += 1

print('--- Keyword Trends (112-114) ---')
report = {}
for y in target_years:
    if y in results:
        print(f'\n[Year {y}] Top 10 Keywords:')
        top10 = results[y].most_common(10)
        report[y] = dict(top10)
        for k, v in top10:
            print(f'  {k}: {v}')
    else:
        print(f'\n[Year {y}] No data')

with open('keyword_trend_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print('\nSaved to keyword_trend_analysis.json')
