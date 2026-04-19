import os

BASE_HTML_PATH = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\templates\base.html"
INDEX_HTML_PATH = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\templates\index.html"

def update_file(path, replacements):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for target, replacement in replacements:
            if target in new_content:
                new_content = new_content.replace(target, replacement)
                print(f"Replaced {target[:30]}...")
            else:
                print(f"Target NOT FOUND in {path}: {target}")
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {path}")
        else:
            print(f"No changes needed for {path}")
            
    except Exception as e:
        print(f"Error updating {path}: {e}")

# Base.html replacements
# Note: Escape quotes carefully in python string literal
# Target: url('{{ url_for('static', filename='images/hero_workspace.svg') }}')
# Replace: url('{{ url_for('static', filename='images/hero_workspace.svg') }}?v=watercolor')

base_replacements = [
    (
        "url('{{ url_for('static', filename='images/hero_workspace.svg') }}')",
        "url('{{ url_for('static', filename='images/hero_workspace.svg') }}?v=watercolor')"
    )
]

# Index.html replacements
# Target: src="{{ url_for('static', filename='images/icon_work.svg') }}"
# Replace: src="{{ url_for('static', filename='images/icon_work.svg') }}?v=watercolor"

index_replacements = [
    (
        'src="{{ url_for(\'static\', filename=\'images/icon_work.svg\') }}"',
        'src="{{ url_for(\'static\', filename=\'images/icon_work.svg\') }}?v=watercolor"'
    ),
    (
        'src="{{ url_for(\'static\', filename=\'images/icon_life.svg\') }}"',
        'src="{{ url_for(\'static\', filename=\'images/icon_life.svg\') }}?v=watercolor"'
    ),
    (
        'src="{{ url_for(\'static\', filename=\'images/icon_videos.svg\') }}"',
        'src="{{ url_for(\'static\', filename=\'images/icon_videos.svg\') }}?v=watercolor"'
    ),
    (
        'src="{{ url_for(\'static\', filename=\'images/icon_podcasts.svg\') }}"',
        'src="{{ url_for(\'static\', filename=\'images/icon_podcasts.svg\') }}?v=watercolor"'
    )
]

if __name__ == "__main__":
    update_file(BASE_HTML_PATH, base_replacements)
    update_file(INDEX_HTML_PATH, index_replacements)
