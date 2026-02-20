import os
import sys

def open_file(path):
    if os.path.exists(path):
        try:
            os.startfile(path)
            print(f"Opening: {path}")
        except Exception as e:
            print(f"Error opening file: {e}")
    else:
        print(f"File not found: {path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Join arguments in case path has spaces and wasn't quoted properly by caller, 
        # though ideally caller handles quoting.
        # But sys.argv[1] should be the path.
        path = " ".join(sys.argv[1:]) 
        open_file(path)
    else:
        print("Usage: python opener.py <file_path>")
