import json
import os
import sys
import docx
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def deep_scan_unknowns(report_path, output_path):
    print(fLoading report from {report_path}...)
    try:
        with open(report_path, r, encoding=utf-8) as f:
            data = json.load(f)
    except Exception as e:
        print(fError loading report: {e})
        return

    unknown_files = []
    if success_data in data:
        for item in data[success_data]:
            meta = item.get(metadata, {})
            if meta.get(year) in [Unknown, None, "]:
 unknown_files.append(item)

 print(fFound {len(unknown_files)} files to scan...)

 results = []
 
 with ThreadPoolExecutor(max_workers=8) as executor:
 future_to_item = {executor.submit(scan_content, item[file_path]): item for item in unknown_files}
 
 for future in as_completed(future_to_item):
 orig = future_to_item[future]
 try:
 y, ev = future.result()
 if y:
 print(f[FOUND {y}] {orig[filename]})
 results.append({
 filename: orig[filename],
 file_path: orig[file_path],
 recovered_year: y,
 evidence: ev
 })
 except Exception:
 pass

 print(fRecovered {len(results)} items.)
 with open(output_path, w, encoding=utf-8) as f:
 json.dump(results, f, ensure_ascii=False, indent=2)
 print(fSaved to {output_path})

def scan_content(path):
 if not os.path.exists(path): return None, None
 try:
 doc = docx.Document(path)
 text = 
 # Limit to 30 paras
 for p in doc.paragraphs[:30]:
 text += p.text + \n
 
 if 111年 in text: return (111, Found 111年)
 if 2022年 in text: return (111, Found 2022年)
 
 # General pattern
 m = re.search(r中華民國\s*([0-9]{2,3})\s*年, text)
 if m: return (m.group(1), ROC Pattern)
 
 m = re.search(r([0-9]{2,3})\s*年度, text)
 if m: return (m.group(1), Year Pattern)

 except: pass
 return None, None

if __name__ == __main__:
 deep_scan_unknowns(batch_scan_report.json, deep_recovery_results.json)
