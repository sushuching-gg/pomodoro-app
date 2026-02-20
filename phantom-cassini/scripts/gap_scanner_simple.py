import json
import os
import sys
import re

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None

def get_meta(filename):
    meta = {'year': 'Unknown', 'city': 'Unknown', 'month': 0}
    
    # Year
    ym = re.search(r'(1[1-4][0-9])', filename)
    if ym: 
        meta['year'] = ym.group(1)
    
    # Month
    # Try date like 1120305 -> Month 03. Must follow the year.
    dm = re.search(r'(1[1-4][0-9])([0-1][0-9])([0-3][0-9])', filename)
    if dm:
        try: 
            m_val = int(dm.group(2))
            if 1 <= m_val <= 12: meta['month'] = m_val
        except: pass
    
    # Try '3月' if date pattern failed
    if meta['month'] == 0:
        mm = re.search(r'([1-9]|1[0-2])月', filename)
        if mm:
            try: meta['month'] = int(mm.group(1))
            except: pass
            
    return meta

def extract_pdf(path):
    if not pdfplumber: return {'error': 'No pdfplumber'}
    try:
        text = ''
        with pdfplumber.open(path) as pdf:
            for i, p in enumerate(pdf.pages):
                if i > 2: break
                t = p.extract_text()
                if t: text += t + '\\n'
        return {'text': text[:500]}
    except Exception as e:
        return {'error': str(e)}

def extract_docx(path):
    if not Document: return {'error': 'No python-docx'}
    try:
        doc = Document(path)
        full = []
        for i, p in enumerate(doc.paragraphs):
            if i > 50: break
            full.append(p.text)
        return {'text': '\\n'.join(full)[:500]}
    except Exception as e:
        return {'error': str(e)}

def main():
    if not os.path.exists('missing_files.json'):
        print('No missing_files.json')
        return
        
    try:
        with open('missing_files.json', 'r', encoding='utf-8') as f:
            files = json.load(f)
    except: return

    results = []
    print(f'Scanning {len(files)} gap files...')
    
    for i, path in enumerate(files):
        if i % 50 == 0: print(f'Processing {i}/{len(files)}...')
        
        path = path.strip()
        if not os.path.exists(path): continue
        
        ext = os.path.splitext(path)[1].lower()
        res = {}
        
        if ext == '.pdf': res = extract_pdf(path)
        elif ext == '.docx': res = extract_docx(path)
        else: continue
        
        if 'error' not in res:
            meta = get_meta(os.path.basename(path))
            results.append({
                'filename': os.path.basename(path),
                'file_path': path,
                'content_summary': res['text'],
                'metadata': meta
            })

    with open('scan_gap_results.json', 'w', encoding='utf-8') as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    print(f'Done. Saved {len(results)} items.')

if __name__ == '__main__':
    main()
