import os
import json
import time

# 支援多個根目錄掃描：包含 D 槽業務資料與當前專案目錄
ROOT_PATHS = [
    r"D:\1_working",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
]
INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_index.json')

def build_index():
    print(f"Building index for: {ROOT_PATHS}...")
    file_list = []
    
    for root_path in ROOT_PATHS:
        if not os.path.exists(root_path):
            print(f"Path not found, skipping: {root_path}")
            continue
            
        print(f"Scanning: {root_path}")
        for root, dirs, files in os.walk(root_path):
            # 排除大型或無關資料夾
            if '.git' in dirs: dirs.remove('.git')
            if '__pycache__' in dirs: dirs.remove('__pycache__')
            if '.gemini' in dirs: dirs.remove('.gemini')
            
            for file in files:
                # 排除暫存檔
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
