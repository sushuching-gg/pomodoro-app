import os
import argparse
import sys

def fix_encoding(target_path):
    if os.path.isfile(target_path):
        _process_file(target_path)
    elif os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            for f in files:
                if f.endswith(('.md', '.txt', '.py', '.csv', '.json')):
                    _process_file(os.path.join(root, f))
    else:
        print(f"Error: Path {target_path} not found.")

def _process_file(file_path):
    try:
        # Try reading as utf-8 first
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            # Fallback to ansi (cp950)
            with open(file_path, 'r', encoding='cp950') as f:
                content = f.read()
        except:
            print(f"Could not read: {file_path}")
            return

    # Write back as utf-8-sig
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print(f"Fixed: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix Windows encoding issues (Garbled text/??)")
    parser.add_argument("--path", required=True, help="Path to file or directory")
    args = parser.parse_args()
    fix_encoding(args.path)
