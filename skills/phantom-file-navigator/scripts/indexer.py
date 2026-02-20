import os
import json
import time

ROOT_PATH = r"D:\1_working"
INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_index.json')

def build_index():
    print(f"Building index for {ROOT_PATH}...")
    file_list = []
    for root, dirs, files in os.walk(ROOT_PATH):
        for file in files:
            if file.startswith("~$"): continue
            try:
                full_path = os.path.join(root, file)
                stat = os.stat(full_path)
                file_list.append({
                    "name": file,
                    "path": full_path,
                    "size": stat.st_size,
                    "modified_ts": stat.st_mtime,
                    "modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
                })
            except Exception:
                continue
    
    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(file_list, f, ensure_ascii=False, indent=2)
        print(f"Index built successfully. Total files: {len(file_list)}")
    except Exception as e:
        print(f"Error saving index: {e}")

if __name__ == "__main__":
    build_index()
