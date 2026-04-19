import os
import shutil

STATIC_IMAGES_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\static\images"
TEMPLATES_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\templates"

MAPPING = {
    "hero_workspace.svg": "hero_workspace_v2.svg",
    "icon_work.svg": "icon_work_v2.svg",
    "icon_life.svg": "icon_life_v2.svg",
    "icon_videos.svg": "icon_videos_v2.svg",
    "icon_podcasts.svg": "icon_podcasts_v2.svg"
}

def rename_images():
    for old_name, new_name in MAPPING.items():
        old_path = os.path.join(STATIC_IMAGES_DIR, old_name)
        new_path = os.path.join(STATIC_IMAGES_DIR, new_name)
        
        if os.path.exists(old_path):
            shutil.copy2(old_path, new_path) # Copy to preserve original just in case, or just rename
            # Let's force rename/overwrite
            print(f"Created/Updated {new_name}")
        else:
            print(f"Warning: {old_name} not found!")

def update_templates():
    for template_name in ["base.html", "index.html"]:
        path = os.path.join(TEMPLATES_DIR, template_name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for old_name, new_name in MAPPING.items():
            # Replace basic filename and also cleanup any query params we added
            # We look for old_name + "?v=watercolor" first
            target_with_query = f"{old_name}?v=watercolor"
            if target_with_query in new_content:
                new_content = new_content.replace(target_with_query, new_name)
            
            # Then replace just the filename if query param wasn't there or was different
            if old_name in new_content:
                 new_content = new_content.replace(old_name, new_name)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {template_name} to use new filenames.")
        else:
            print(f"No changes needed for {template_name}")

if __name__ == "__main__":
    rename_images()
    update_templates()
