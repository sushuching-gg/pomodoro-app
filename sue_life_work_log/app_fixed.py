from datetime import datetime
from werkzeug.utils import secure_filename
import os, frontmatter, markdown, mimetypes
from flask import Flask, render_template, render_template_string, abort, request, redirect, url_for, send_from_directory, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "sue2026"
ADMIN_PASSWORD = "sue2026"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
WORK_DIR = os.path.join(CONTENT_DIR, "work")

def get_files(directory):
    files = []
    if not os.path.exists(directory): return []
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            try:
                with open(os.path.join(directory, filename), "r", encoding="utf-8-sig") as f:
                    post = frontmatter.load(f)
                    files.append({"filename": filename, "date": post.get("date"), "title": post.get("title") or filename, "content": markdown.markdown(post.content)})
            except: pass
    files.sort(key=lambda x: str(x["date"]), reverse=True)
    return files

@app.route("/")
def index():
    return render_template("index.html", work=get_files(WORK_DIR)[:3])

@app.route("/admin")
@admin_required
def admin_list():
    return "Admin Panel"

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_list"))
    return "<h2>Login</h2><form method=POST><input type=password name=password><button>OK</button></form>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
