import json
import collections

def analyze():
    items = []
    try:
        with open('merged_admin_data.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
            items = d.get('success_data', [])
    except:
        try:
            with open('merged_admin_data.json', 'r', encoding='cp950', errors='ignore') as f:
                d = json.load(f)
                items = d.get('success_data', [])
        except: return

    anchors = {'112': 8, '113': 4, '114': 2}
    
    cats = {
        'Coaching': ['輔導', '訪視', '座談', '工作坊', '共識營', '諮詢'],
        'Review': ['審查', '意見', '回覆', '修正', '核定', '評選', '初審', '複審'],
        'Briefing': ['說明會', '申請須知', '徵件', '招標']
    }

    timeline = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

    for item in items:
        meta = item.get('metadata', {})
        y = meta.get('year', 'Unknown')
        if y not in anchors: continue
        
        try:
            m = int(meta.get('month', '0'))
        except: continue
        if m == 0: continue
        
        text = (item.get('filename', '') + ' ' + item.get('content_summary', '')).lower()
        
        # Categorize
        if any(w in text for w in cats['Coaching']): c = 'Coaching'
        elif any(w in text for w in cats['Review']): c = 'Review'
        elif any(w in text for w in cats['Briefing']): c = 'Briefing'
        else: continue
            
        base = anchors[y]
        rel = m - base
        timeline[y][rel][c] += 1

    print('# Event-Driven Admin Analysis')
    print('Baseline (T=0) = County Briefing Month')
    
    for y in sorted(anchors.keys()):
        base = anchors[y]
        print(f'\n## Year {y} (Briefing: Month {base})')
        
        for t in range(-2, 8):
            actual_m = base + t
            label = f'T{t}' if t < 0 else f'T+{t}'
            if t == 0: label += '[Event]'
            
            c_coach = timeline[y][t]['Coaching']
            c_rev = timeline[y][t]['Review']
            c_brief = timeline[y][t]['Briefing']
            
            # Skip empty months
            if c_coach + c_rev + c_brief == 0: continue

            out = f'  {label:<12} (Month {actual_m}): '
            if c_brief: out += f'Briefing={c_brief} '
            if c_coach: out += f'Coaching={c_coach} '
            if c_rev:   out += f'Review={c_rev} '
            print(out)

if __name__ == '__main__':
    analyze()
