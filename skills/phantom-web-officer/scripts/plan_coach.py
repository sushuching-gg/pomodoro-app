import argparse
import os
import sys

# Ensure current directory is in path to import plan_parser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from plan_parser import parse_plan
except ImportError:
    # Fallback or error handling if parser is missing
    def parse_plan(path):
        return {"error": "Parser module not found"}

def analyze_plan(draft_path, plan_type):
    print(f"=== Phantom Plan Coach ===")
    print(f"Analyzing Draft: {draft_path} (Type: {plan_type})")
    
    if not os.path.exists(draft_path):
        print("Error: File not found.")
        return

    # 1. Parsing
    try:
        data = parse_plan(draft_path)
    except Exception as e:
        print(f"Parsing Failed: {e}")
        return

    if "error" in data:
        print(f"System Error: {data['error']}")
        return

    # 2. Extract Info
    metadata = data.get('metadata', {})
    summary = data.get('content_summary', '')
    tables = data.get('tables', [])
    
    # 3. Validation Rules
    issues = []
    score = 0
    
    print("\n[Structure Check]")
    
    # Rule 1: Metadata Check
    year = metadata.get('year')
    city = metadata.get('city')
    if year and city:
        print(f"[v] Identified: {year} Year {city} Plan")
        score += 20
    else:
        print(f"[x] Warning: Cannot identify Year or City from filename")
        issues.append("Filename convention error")

    # Rule 2: Budget Check
    budget_table = next((t for t in tables if t['type'] == 'budget_candidate'), None)
    total_amount = "Unknown"
    
    if budget_table:
        try:
            rows = budget_table['content']
            if rows:
                last_row = rows[-1]
                for cell in reversed(last_row):
                   if any(char.isdigit() for char in cell):
                       total_amount = cell
                       break
            
            print(f"[v] Budget Table Found: {len(rows)} rows")
            print(f"  - Est. Total: {total_amount}")
            score += 40
        except:
            print(f"[v] Budget Table Found (Parsing issues)")
            score += 30
    else:
        print("[x] Critical: No Budget Table found")
        issues.append("Missing Budget Table")

    # Rule 3: Keywords
    keywords = ["AI", "數據", "人工智慧", "大數據", "物聯網", "IoT", "穿戴式"]
    found_keywords = [kw for kw in keywords if kw in summary]
    
    print("\n[Content Suggestions]")
    if found_keywords:
        print(f"[v] Digital Transformation Elements: {', '.join(found_keywords)}")
        score += 30
    else:
        print("- Suggestion: Add 'Innovation Strategy' chapter with AI/Data keywords.")
        issues.append("Lack of Innovation Elements")

    # Final Score
    score += 10
    if score > 100: score = 100
    
    print("\n[Quality Score]")
    print(f"Auto-Score: {score}/100")
    
    if score < 60:
        print("Result: Fail (Major Issues)")
    elif score < 80:
        print("Result: Fair (Needs Improvement)")
    else:
        print("Result: Good (Compliant)")

    if issues:
        print(f"Pending Fixes: {', '.join(issues)}")
    else:
        print("Suggestion: Ready for submission.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True, help="Draft path")
    parser.add_argument("--type", default="general", help="Plan type")
    args = parser.parse_args()
    
    analyze_plan(args.draft, args.type)
