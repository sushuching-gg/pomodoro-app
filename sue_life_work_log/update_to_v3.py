import os

TEMPLATES_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\templates"

MAPPING = {
    "hero_workspace": "hero_workspace_v3.svg",
    "icon_work": "icon_work_v3.svg",
    "icon_life": "icon_life_v3.svg",
    "icon_videos": "icon_videos_v3.svg",
    "icon_podcasts": "icon_podcasts_v3.svg"
}

def update_templates():
    for template_name in ["base.html", "index.html"]:
        path = os.path.join(TEMPLATES_DIR, template_name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        # We need to replace potentially any previous versions (v1, v2)
        # Regex or simple string search. Since we know the previous step used specific filenames...
        
        # Replace hero
        if "hero_workspace" in new_content:
            # This is a bit risky if we don't match the full filename pattern, but let's try to be specific
            # Finding: filename='images/hero_workspace*.svg'
            import re
            new_content = re.sub(r"filename='images/hero_workspace.*?\.svg'", f"filename='images/{MAPPING['hero_workspace']}'", new_content)

        # Replace icons
        for key, val in MAPPING.items():
            if key == "hero_workspace": continue
            # filename='images/icon_work*.svg'
            new_content = re.sub(f"filename='images/{key}.*?\.svg'", f"filename='images/{val}'", new_content)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {template_name} to use V3 filenames.")
        else:
            print(f"No changes needed for {template_name}")

if __name__ == "__main__":
    update_templates()
