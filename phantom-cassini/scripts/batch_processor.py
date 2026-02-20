import os
import sys
import json
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "..", "..", "skills", "phantom-web-officer", "scripts"))

try:
    from plan_parser import parse_plan
except ImportError:
    print("Error: Could not import plan_parser.")
    sys.exit(1)

def safe_print(message):
    try:
        print(message)
    except Exception:
        # Fallback to ascii-only representation to guarantee it prints
        try:
            print(message.encode('cp950', 'replace').decode('cp950'))
        except:
             print(ascii(message))

def process_file(file_path):
    try:
        if os.path.basename(file_path).startswith("~$"):
            return None
            
        result = parse_plan(file_path)
        
        if "error" in result:
             return {"status": "error", "file": file_path, "message": result['error']}
             
        if 'tables' in result:
            count = len(result['tables'])
            result['table_count'] = count
            del result['tables']

        return {"status": "success", "file": file_path, "data": result}
        
    except Exception as e:
        return {"status": "error", "file": file_path, "message": str(e)}

def batch_process(root_dir):
    safe_print(f"Scanning directory: {root_dir}")
    
    docx_files = glob.glob(os.path.join(root_dir, "**", "*.docx"), recursive=True)
    safe_print(f"Found {len(docx_files)} DOCX files in total.")
    
    results = {
        "summary": {"total": 0, "success": 0, "error": 0},
        "success_data": [],
        "errors": []
    }
    
    output_file="batch_scan_report.json"

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in docx_files}
        
        for i, future in enumerate(as_completed(future_to_file)):
            file_path = future_to_file[future]
            try:
                res = future.result()
                if res:
                    if res['status'] == 'success':
                        results['success_data'].append(res['data'])
                        results['summary']['success'] += 1
                        safe_print(f"[OK] {os.path.basename(file_path)}")
                    else:
                        results['errors'].append(res)
                        results['summary']['error'] += 1
                        safe_print(f"[FAIL] {os.path.basename(file_path)}: {res['message']}")
            except Exception as exc:
                results['errors'].append({"status": "error", "file": file_path, "message": str(exc)})
                results['summary']['error'] += 1
                safe_print(f"[FAIL] {os.path.basename(file_path)}: Exception {exc}")
            
            results['summary']['total'] += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    safe_print(f"\nBatch processing complete.")
    safe_print(f"Total: {results['summary']['total']}")
    safe_print(f"Success: {results['summary']['success']}")
    safe_print(f"Errors: {results['summary']['error']}")
    safe_print(f"Report saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_processor.py <root_directory>")
        sys.exit(1)
        
    root_dir = sys.argv[1]
    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        sys.exit(1)
        
    batch_process(root_dir)
