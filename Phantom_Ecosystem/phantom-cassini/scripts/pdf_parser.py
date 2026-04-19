import json
import os
import sys
import re
try:
    import pdfplumber
except ImportError:
    print('Error: pdfplumber not installed')
    sys.exit(1)

def parse_pdf(pdf_path):
    print(f'Parsing PDF: {pdf_path}')
    
    data = {
        'file_path': pdf_path,
        'filename': os.path.basename(pdf_path),
        'metadata': {'year': 'Unknown', 'city': 'Unknown'},
        'doc_type': 'proposal',
        'content_summary': '',
        'tables': [],
    }
    
    if any(kw in data['filename'] for kw in ['審查', '意見', '彙整', '回覆']):
        data['doc_type'] = 'review_form'

    year_match = re.search(r'(1[0-2][0-9])年', data['filename'])
    if year_match:
        data['metadata']['year'] = year_match.group(1)
    else:
        ad_match = re.search(r'(20[1-3][0-9])年?', data['filename'])
        if ad_match:
            data['metadata']['year'] = str(int(ad_match.group(1)) - 1911)
            
    cities = ['臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市', 
              '基隆市', '新竹市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', 
              '雲林縣', '嘉義縣', '嘉義市', '屏東縣', '宜蘭縣', '花蓮縣', 
              '臺東縣', '澎湖縣', '金門縣', '連江縣']

    for city in cities:
        if city in data['filename']:
            data['metadata']['city'] = city
            break

    try:
        full_text = []
        with pdfplumber.open(pdf_path) as pdf:
            max_pages = min(len(pdf.pages), 10)
            
            for i in range(max_pages):
                page = pdf.pages[i]
                text = page.extract_text()
                if text:
                    full_text.append(text)
                
                tables = page.extract_tables()
                if tables:
                    for t_idx, table in enumerate(tables):
                        if table and len(table) > 0 and table[0]:
                            header_str = ''.join([str(c) for c in table[0] if c])
                            budget_keywords = ['經費', '預算', '單價', '金額', '費用', 'Capital']
                            if any(kw in header_str for kw in budget_keywords):
                                data['tables'].append({
                                    'page': i + 1,
                                    'index': t_idx,
                                    'content': table
                                })

        text_content = '\n'.join(full_text)
        data['content_summary'] = text_content[:500].replace('\n', ' ')

        # Deep Metadata Extraction from Text
        if data['metadata']['year'] == 'Unknown':
            roc_match = re.search(r'中華民國\s*([0-9]{2,3})\s*年', text_content)
            if roc_match:
                data['metadata']['year'] = roc_match.group(1)
            if data['metadata']['year'] == 'Unknown':
                if '111' in text_content or '2022' in text_content:
                     data['metadata']['year'] = '111'

        if data['metadata']['city'] == 'Unknown':
            for city in cities:
                if city in text_content:
                    data['metadata']['city'] = city
                    break

    except Exception as e:
        return {'file': pdf_path, 'error': str(e)}
    
    return data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python pdf_parser.py <pdf_path>')
        sys.exit(1)
        
    res = parse_pdf(sys.argv[1])
    print(json.dumps(res, ensure_ascii=False, indent=2))
