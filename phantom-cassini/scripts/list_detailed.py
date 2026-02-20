import json
import collections

def main():
    try:
        with open('merged_admin_data_final.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
            items = d.get('success_data', [])
    except:
        print('No data')
        return

    cats = {
        'Visit': ['訪視', '三書', '比對', '需求', '建議書', '成果', '查核', '督導'],
        'Review': ['審查', '意見', '回覆', '修正', '核定', '評選', '初審', '複審'],
        'Briefing': ['說明會', '申請須知', '徵件', '招標'],
        'Coaching': ['輔導', '座談', '工作坊']
    }

    # Data Struct: Year -> Month -> {Category: [File List]}
    data = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))

    for item in items:
        meta = item.get('metadata', {})
        y = str(meta.get('year', 'Unknown'))
        try: m = int(meta.get('month', 0))
        except: continue
        if m == 0 or y not in ['112', '113', '114']: continue

        text = (item.get('filename', '') + ' ' + item.get('content_summary', '')).lower()
        
        c = 'Other'
        if any(w in text for w in cats['Briefing']): c = 'Briefing'
        elif any(w in text for w in cats['Visit']): c = 'Visit'
        elif any(w in text for w in cats['Review']): c = 'Review'
        elif any(w in text for w in cats['Coaching']): c = 'Coaching'
        
        if c != 'Other':
            data[y][m][c].append(item.get('filename', 'Unknown'))

    print('# Detailed Work Breakdown List')
    
    for y in sorted(data.keys()):
        print(f'\n## Year {y}')
        for m in sorted(data[y].keys()):
            month_dict = data[y][m]
            if not month_dict: continue
            
            print(f'\n### Month {m}')
            for c in sorted(month_dict.keys()):
                files = list(set(month_dict[c])) # Unique
                count = len(files)
                ex_str = ', '.join(files[:3])
                if len(files) > 3: ex_str += '...'
                print(f'- **{c}** ({count}): {ex_str}')

if __name__ == '__main__':
    main()
