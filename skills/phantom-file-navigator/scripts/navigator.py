import os
import json
import sys

INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_index.json')

def search(query):
    if not os.path.exists(INDEX_FILE):
        print("Index not found. Please run indexer.py first.")
        return

    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            file_index = json.load(f)
    except Exception as e:
         print(f"Error loading index: {e}")
         return
        
    query_parts = query.lower().split()
    results = []
    
    for file in file_index:
        fname = file['name'].lower()
        if all(part in fname for part in query_parts):
            results.append(file)
    
    results.sort(key=lambda x: x['modified_ts'], reverse=True)
    
    print(f"Found {len(results)} results for '{query}':")
    for res in results[:20]:
        print(f"[{res['modified']}] {res['name']}")
        print(f"   Path: {res['path']}")
        print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == 'search':
        search(" ".join(sys.argv[2:]))
    else:
        print("Usage: python navigator.py search <keywords>")
