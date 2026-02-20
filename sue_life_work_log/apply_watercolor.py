import os
import random

# Configuration
# Pointing to the correct static images directory
TARGET_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\static\images"

FILES_CONFIG = [
    {
        "filename": "hero_workspace.svg",
        "width": 800,
        "height": 400,
        "base_hue": 35,
        "hue_variation": 15,
        "is_hero": True
    },
    {
        "filename": "icon_work.svg",
        "width": 200,
        "height": 200,
        "base_hue": 210,
        "hue_variation": 15,
        "is_hero": False
    },
    {
        "filename": "icon_life.svg",
        "width": 200,
        "height": 200,
        "base_hue": 355,
        "hue_variation": 15,
        "is_hero": False
    },
    {
        "filename": "icon_videos.svg",
        "width": 200,
        "height": 200,
        "base_hue": 270,
        "hue_variation": 20,
        "is_hero": False
    },
    {
        "filename": "icon_podcasts.svg",
        "width": 200,
        "height": 200,
        "base_hue": 50,
        "hue_variation": 10,
        "is_hero": False
    }
]

WATERCOLOR_FILTERS = """
<defs>
    <filter id="watercolor">
        <feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="3" result="noise" />
        <feDisplacementMap in="SourceGraphic" in2="noise" scale="5" xChannelSelector="R" yChannelSelector="G" />
        <feGaussianBlur stdDeviation="0.5" />
    </filter>
</defs>
"""

def hsv_to_rgb_hex(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
        
    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)
    return f"#{r:02x}{g:02x}{b:02x}"

def generate_blobs(width, height, base_hue, hue_var, num_blobs=60):
    blobs = []
    blobs.append(f'<rect width="{width}" height="{height}" fill="#fff" opacity="0.1" />')
    
    for _ in range(num_blobs):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        # Center bias
        if random.random() > 0.4:
            cx = (cx + width/2) / 2
            cy = (cy + height/2) / 2
            
        rx = random.randint(width // 12, width // 3)
        ry = random.randint(height // 12, height // 3)
        rotation = random.randint(0, 360)
        
        hue = base_hue + random.uniform(-hue_var, hue_var)
        sat = random.uniform(0.2, 0.5)
        val = random.uniform(0.9, 1.0)
        color = hsv_to_rgb_hex(hue, sat, val)
        opacity = random.uniform(0.05, 0.15)
        
        blobs.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" fill-opacity="{opacity}" transform="rotate({rotation} {cx} {cy})" />')
        
    return "\n".join(blobs)

def process_file(config):
    filepath = os.path.join(TARGET_DIR, config["filename"])
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"Processing {config['filename']}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    bg_svg = generate_blobs(config["width"], config["height"], config["base_hue"], config["hue_variation"])
    
    # Reconstruct SVG
    new_svg = [f'<svg width="{config["width"]}" height="{config["height"]}" viewBox="0 0 {config["width"]} {config["height"]}" xmlns="http://www.w3.org/2000/svg">']
    new_svg.append(WATERCOLOR_FILTERS)
    new_svg.append(f'<g id="watercolor-bg">{bg_svg}</g>')
    new_svg.append('<g filter="url(#watercolor)">')
    
    lines = content.split('\n')
    for line in lines:
        sline = line.strip()
        if sline.startswith('<svg') or sline.startswith('</svg'): continue
        if config["is_hero"]:
            if 'fill="#FDF5E6"' in line or 'fill="#DEB887"' in line: continue
        else:
            if '<circle' in line and 'r="95"' in line: continue
        new_svg.append(line)
        
    new_svg.append('</g>')
    new_svg.append('</svg>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_svg))
    print(f"Updated {config['filename']}")

if __name__ == "__main__":
    for config in FILES_CONFIG:
        process_file(config)
