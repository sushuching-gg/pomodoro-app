import os
import datetime

BASE_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log"
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, "static", "images")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
INDEX_PATH = os.path.join(TEMPLATES_DIR, "index.html")

SCENES = {
    "work": "work_scene_watercolor.svg",
    "life": "life_scene_watercolor.svg",
    "videos": "videos_scene_watercolor.svg",
    "podcasts": "podcasts_scene_watercolor.svg"
}

def get_svg_content(filename):
    path = os.path.join(STATIC_IMAGES_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def embed_svgs_in_index():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to find the <img> tags and replace them with the inline SVG content.
    # The current tags look like: <img src="{{ ... }}" alt="Work" style="...">
    # We will use regex to find them and replace with a div containing the svg.
    
    import re
    
    # Common style for the embedded SVGs to match the previous img dimensions
    svg_style = 'style="width: 50px; height: 50px; margin-right: 15px;"'
    
    for key, filename in SCENES.items():
        svg_xml = get_svg_content(filename)
        # We need to make sure the SVG tag itself has the style attributes or is wrapped
        # The raw SVGs have width="400" height="300" etc. We want to force them to 50x50 displayed.
        # So we can wrap them: <div style="width: 50px; ..."> <svg ... width="100%" height="100%" ...> </svg> </div>
        # Or just modify the SVG tag. Let's wrap for safety.
        
        # Inject "preserveAspectRatio" and override width/height for responsive scaling in the wrapper
        # Actually simplest is to just drop it in a div of fixed size.
        
        # Modify the raw SVG to fit container? 
        # Let's just wrap it.
        replacement = f'<div class="icon-wrapper" style="width: 60px; height: 50px; margin-right: 15px; display: flex; align-items: center; justify-content: center; overflow: hidden;">{svg_xml}</div>'
        
        # Regex to match the existing img tag for this section
        # We look for the alt tag to identify the specific section image
        # alt="Work", alt="Life", alt="Travel", alt="Videos", alt="Podcasts"
        
        alt_map = {
            "work": "Work",
            "life": "Life",
            "videos": "Videos",
            "podcasts": "Podcasts"
        }
        
        target_alt = alt_map.get(key)
        if target_alt:
            # Pattern: <img [^>]*alt="Work"[^>]*>
            pattern = f'<img [^>]*alt="{target_alt}"[^>]*>'
            
            # Special handling for Life since it appears twice (once for "Life", once for "Travel")
            # The "Travel" one has alt="Travel"
            if key == "life":
                # Do standard Life
                content = re.sub(f'<img [^>]*alt="Life"[^>]*>', replacement, content)
                # Do Travel (uses same SVG)
                content = re.sub(f'<img [^>]*alt="Travel"[^>]*>', replacement, content)
            else:
                content = re.sub(pattern, replacement, content)
                
    # Also update footer to verify reload
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    footer_tag = '&copy; 2026 Sue\'s Life & Work Log.'
    new_footer = f'&copy; 2026 Sue\'s Life & Work Log. (Updated: {timestamp})'
    content = content.replace(footer_tag, new_footer)

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Embedded SVGs into index.html inline.")

if __name__ == "__main__":
    embed_svgs_in_index()
