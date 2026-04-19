import os

TEMPLATES_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\templates"

# Mapping specific for scene illustrations this time
MAPPING = {
    # Keep hero as hero_workspace_v3.svg since the prompt was for a scene and it was decently complex
    # But let's rename the others to the scene versions
    "icon_work": "work_scene_watercolor.svg",
    "icon_life": "life_scene_watercolor.svg",
    "icon_videos": "videos_scene_watercolor.svg",
    "icon_podcasts": "podcasts_scene_watercolor.svg"
}

def update_templates_scenes():
    for template_name in ["base.html", "index.html"]:
        path = os.path.join(TEMPLATES_DIR, template_name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        import re

        # Helper to replace filename regardless of v2/v3 suffix
        # Pattern: filename='images/icon_work.*?.svg'  -> filename='images/work_scene_watercolor.svg'
        
        for key, val in MAPPING.items():
            # If key is "icon_work", we want to match "icon_work_v3.svg", "icon_work.svg", etc.
            pattern = f"filename='images/{key}.*?\.svg'"
            replacement = f"filename='images/{val}'"
            
            # Use regex sub
            new_content = re.sub(pattern, replacement, new_content)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {template_name} to use Scene filenames.")
        else:
            print(f"No changes needed for {template_name}")

if __name__ == "__main__":
    update_templates_scenes()
