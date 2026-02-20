from datetime import datetime
from werkzeug.utils import secure_filename
import os
import frontmatter
import markdown
import mimetypes
from flask import Flask, render_template, abort, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Use absolute paths to avoid confusion
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
WORK_DIR = os.path.join(CONTENT_DIR, "work")
LIFE_TRAVEL_DIR = os.path.join(CONTENT_DIR, "life", "travel")
LIFE_DAILY_ME_DIR = os.path.join(CONTENT_DIR, "life", "daily", "me")
LIFE_DAILY_GRANDMA_DIR = os.path.join(CONTENT_DIR, "life", "daily", "grandma")
VIDEOS_DIR = os.path.join(CONTENT_DIR, "videos")
PODCASTS_DIR = os.path.join(CONTENT_DIR, "podcasts")
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, "static", "images")

# Ensure directories exist
for d in [WORK_DIR, LIFE_TRAVEL_DIR, LIFE_DAILY_ME_DIR, LIFE_DAILY_GRANDMA_DIR, VIDEOS_DIR, PODCASTS_DIR, STATIC_IMAGES_DIR]:
    os.makedirs(d, exist_ok=True)

def get_files(directory):
    files = []
    if not os.path.exists(directory):
        return files
        
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                    files.append({
                        "filename": filename,
                        "date": post.get("date"),
                        "title": post.get("title") or filename.replace("-", " ").title(),
                        "type": post.get("type"),
                        "content": markdown.markdown(post.content),
                        "metadata": post.metadata
                    })
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                
    # Sort by date descending
    files.sort(key=lambda x: str(x["date"]), reverse=True)
    return files

def get_dir_by_category(category):
    if category == "work": return WORK_DIR
    elif category == "life_travel": return LIFE_TRAVEL_DIR
    elif category == "life_daily_me": return LIFE_DAILY_ME_DIR
    elif category == "life_daily_grandma": return LIFE_DAILY_GRANDMA_DIR
    elif category == "videos": return VIDEOS_DIR
    elif category == "podcasts": return PODCASTS_DIR
    return None

@app.route("/")
def index():
    # Show recent items from all major categories
    work = get_files(WORK_DIR)
    daily_me = get_files(LIFE_DAILY_ME_DIR)
    daily_grandma = get_files(LIFE_DAILY_GRANDMA_DIR)
    travel = get_files(LIFE_TRAVEL_DIR)
    videos = get_files(VIDEOS_DIR)
    podcasts = get_files(PODCASTS_DIR)
    
    return render_template("index.html", work=work[:3], daily_me=daily_me[:3], daily_grandma=daily_grandma[:3], travel=travel[:3], videos=videos[:3], podcasts=podcasts[:3])

@app.route("/work")
def work():
    items = get_files(WORK_DIR)
    return render_template("list.html", title="Work Logs (工作日誌)", items=items, category="work")

@app.route("/life")
def life():
    # Redirect to Daily Me as default view for Life, but eventually could be a dashboard
    return redirect(url_for('life_daily_me'))

@app.route("/life/travel")
def life_travel():
    items = get_files(LIFE_TRAVEL_DIR)
    return render_template("list.html", title="Life: Travel (旅遊)", items=items, category="life_travel")

@app.route("/life/daily/me")
def life_daily_me():
    items = get_files(LIFE_DAILY_ME_DIR)
    return render_template("list.html", title="Life: Daily Me (我的生活)", items=items, category="life_daily_me")

@app.route("/life/daily/grandma")
def life_daily_grandma():
    items = get_files(LIFE_DAILY_GRANDMA_DIR)
    return render_template("list.html", title="Life: Grandma (阿嬤的生活)", items=items, category="life_daily_grandma")

@app.route("/videos")
def videos():
    items = get_files(VIDEOS_DIR)
    return render_template("list.html", title="Video Projects", items=items, category="videos")

@app.route("/podcasts")
def podcasts():
    items = get_files(PODCASTS_DIR)
    return render_template("list.html", title="Podcasts", items=items, category="podcasts")

@app.route("/entry/<category>/<filename>")
def view_entry(category, filename):
    target_dir = get_dir_by_category(category)
    if not target_dir: abort(404)
        
    filepath = os.path.join(target_dir, filename)
    if not os.path.exists(filepath): abort(404)
        
    with open(filepath, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
        html_content = markdown.markdown(post.content)
        
    return render_template("entry.html", post=post, content=html_content, category=category)

# --- Admin Routes ---

@app.route("/admin")
def admin_list():
    files = {
        "work": get_files(WORK_DIR),
        "life_travel": get_files(LIFE_TRAVEL_DIR),
        "life_daily_me": get_files(LIFE_DAILY_ME_DIR),
        "life_daily_grandma": get_files(LIFE_DAILY_GRANDMA_DIR),
        "videos": get_files(VIDEOS_DIR),
        "podcasts": get_files(PODCASTS_DIR)
    }
    return render_template("admin_list.html", files=files, title="後台管理")

@app.route("/admin/edit/<category>/<filename>")
def admin_edit(category, filename):
    target_dir = get_dir_by_category(category)
    if not target_dir: abort(404)
        
    filepath = os.path.join(target_dir, filename)
    if not os.path.exists(filepath): abort(404)
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    return render_template("admin_edit.html", content=content, filename=filename, category=category, title=f"編輯 {filename}")

@app.route("/admin/save", methods=["POST"])
def admin_save():
    category = request.form.get("category")
    filename = request.form.get("filename")
    content = request.form.get("content")
    
    target_dir = get_dir_by_category(category)
    if not target_dir or not filename or not content: abort(400)
    
    filepath = os.path.join(target_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.replace('\r\n', '\n'))
        
    return redirect(url_for("admin_list"))

@app.route("/admin/delete/<category>/<filename>", methods=["POST"])
def admin_delete(category, filename):
    target_dir = get_dir_by_category(category)
    if not target_dir: abort(404)
        
    filepath = os.path.join(target_dir, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
            abort(500)
            
    return redirect(url_for("admin_list"))


@app.route("/content/<path:filename>")
def serve_content(filename):
    return send_from_directory(CONTENT_DIR, filename)

@app.route("/admin/upload", methods=["GET", "POST"])
def admin_upload():
    if request.method == "POST":
        file = request.files.get("file")
        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description", "")
        
        if not title or not category:
            return "Missing info", 400
        
        md_filename = ""
        html_embed = ""
        
        # Determine target directory based on category
        target_dir = get_dir_by_category(category)
        if not target_dir:
            return "Invalid Category", 400

        # Create a safe title for filename if no file is provided
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = secure_filename(title) 
        if not safe_title: safe_title = "entry"

        # Handle File Upload
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            md_filename = os.path.splitext(filename)[0] + ".md" 
            
            # Determine file type
            mimetype = file.content_type
            if not mimetype:
                mimetype, _ = mimetypes.guess_type(filename)
                
            # Logic: Upload file to appropriate media folder, but save MD in category folder
            # We will use VIDEOS_DIR and PODCASTS_DIR as storage for large media even if category is "work"
            
            if mimetype and mimetype.startswith('video'):
                file.save(os.path.join(VIDEOS_DIR, filename))
                html_embed = f'<video controls width="100%"><source src="/content/videos/{filename}" type="{mimetype}"></video>'
                
            elif mimetype and mimetype.startswith('audio'):
                file.save(os.path.join(PODCASTS_DIR, filename))
                html_embed = f'<audio controls style="width: 100%"><source src="/content/podcasts/{filename}" type="{mimetype}"></audio>'
                
            else:
                # Default to image
                image_path = os.path.join(STATIC_IMAGES_DIR, filename)
                file.save(image_path)
                html_embed = f'![{title}](/static/images/{filename})'
        else:
            # No file, just text
            md_filename = f"{date_str}-{safe_title}.md"

        # Save Markdown File to the SELECTED CATEGORY directory
        md_path = os.path.join(target_dir, md_filename)
        
        md_content = f'''---
title: {title}
date: {date_str}
type: {category}
---

{html_embed}

{description}
'''
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        return redirect(url_for("admin_list"))
        
    return render_template("admin_upload.html", title="Upload / New Entry")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
