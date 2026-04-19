import os, time, logging, frontmatter, markdown, socket, ctypes
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps
from flask import Flask, render_template, render_template_string, abort, request, redirect, url_for, send_from_directory, session, flash
from datetime import timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'sue2026-secret-key-12345'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_NAME'] = 'sue_log_session_v3'
ADMIN_PASSWORD = 'sue2026'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')

CATEGORIES = {
    'work':               os.path.join(CONTENT_DIR, 'work'),
    'life_travel':        os.path.join(CONTENT_DIR, 'life', 'travel'),
    'life_daily_me':      os.path.join(CONTENT_DIR, 'life', 'daily', 'me'),
    'life_daily_grandma': os.path.join(CONTENT_DIR, 'life', 'daily', 'grandma'),
    'videos':             os.path.join(CONTENT_DIR, 'videos'),
    'podcasts':           os.path.join(CONTENT_DIR, 'podcasts'),
}

for _d in list(CATEGORIES.values()) + [STATIC_IMAGES_DIR]:
    os.makedirs(_d, exist_ok=True)

def safe_path(base_dir, filename):
    real_base = os.path.realpath(base_dir)
    real_path = os.path.realpath(os.path.join(base_dir, filename))
    if not real_path.startswith(real_base + os.sep) and real_path != real_base:
        abort(403)
    return real_path

_FILE_CACHE = {}
_CACHE_TTL = 30

def _load_files_from_disk(directory):
    files = []
    if not os.path.exists(directory): return files
    for filename in sorted(os.listdir(directory), reverse=True):
        if not filename.endswith('.md'): continue
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                post = frontmatter.load(f)
            files.append({ 'filename': filename, 'date': post.get('date'), 'title': post.get('title') or filename, 'content': markdown.markdown(post.content) })
        except Exception as e:
            logger.warning('[get_files] Parse failed: %s - %s', filename, e)
    files.sort(key=lambda x: str(x.get('date') or ''), reverse=True)
    return files

def get_files(directory, limit=None):
    if not os.path.exists(directory): return []
    try: mtime = os.path.getmtime(directory)
    except OSError: mtime = 0
    now = time.time()
    cached = _FILE_CACHE.get(directory)
    if cached and cached['mtime'] == mtime and (now - cached['ts']) < _CACHE_TTL:
        files = cached['data']
    else:
        files = _load_files_from_disk(directory)
        _FILE_CACHE[directory] = { 'data': files, 'mtime': mtime, 'ts': now }
    return files[:limit] if limit is not None else files

def invalidate_cache(directory):
    _FILE_CACHE.pop(directory, None)

def get_dir_by_category(category):
    return CATEGORIES.get(category)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def check_login():
    white_list = ['admin_login', 'static', 'serve_image']
    if request.endpoint not in white_list and not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

@app.route('/')
@admin_required
def index():
    return render_template('index.html', work=get_files(CATEGORIES['work'], limit=3), daily_me=get_files(CATEGORIES['life_daily_me'], limit=3), travel=get_files(CATEGORIES['life_travel'], limit=3))

@app.route('/work')
@admin_required
def work():
    return render_template('list.html', title='Work Logs', items=get_files(CATEGORIES['work']), category='work')

@app.route('/life/travel')
@app.route('/life_travel')
@admin_required
def life_travel():
    return render_template('list.html', title='Travel Adventures', items=get_files(CATEGORIES['life_travel']), category='life_travel')

@app.route('/life/daily/me')
@app.route('/life_daily_me')
@admin_required
def life_daily_me():
    return render_template('list.html', title='My Stories', items=get_files(CATEGORIES['life_daily_me']), category='life_daily_me')

@app.route('/life/daily/grandma')
@app.route('/life_daily_grandma')
@admin_required
def life_daily_grandma():
    return render_template('list.html', title='Grandma\'s Daily', items=get_files(CATEGORIES['life_daily_grandma']), category='life_daily_grandma')

@app.route('/videos')
@admin_required
def videos():
    return render_template('list.html', title='Videos', items=get_files(CATEGORIES['videos']), category='videos')

@app.route('/podcasts')
@admin_required
def podcasts():
    return render_template('list.html', title='Podcasts', items=get_files(CATEGORIES['podcasts']), category='podcasts')

@app.route('/entry/<category>/<filename>')
@admin_required
def entry(category, filename):
    target_dir = get_dir_by_category(category)
    if not target_dir: abort(404)
    filepath = safe_path(target_dir, filename)
    if not os.path.exists(filepath): abort(404)
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            post = frontmatter.load(f)
        content_html = markdown.markdown(post.content, extensions=['extra'])
        return render_template('entry.html', post=post, category=category, filename=filename, content=content_html)
    except Exception as e:
        logger.error('[entry] Error: %s', e)
        abort(500)

@app.route('/entry/<category>/media/<path:filename>')
@admin_required
def serve_entry_media(category, filename):
    target_dir = get_dir_by_category(category)
    if not target_dir: abort(404)
    return send_from_directory(target_dir, filename)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'): return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session.permanent = True
            session['admin_logged_in'] = True
            return redirect(url_for('index'))
        flash('密碼錯誤，請重試')
    return render_template_string("""
    <html>
    <head><title>Admin Login</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="text-align:center;padding-top:100px;background:#f9f7f2;font-family:sans-serif;">
        <div style="max-width:300px;margin:0 auto;background:white;padding:30px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
            <h2>旅刻日誌安全入駐</h2>
            <p style="color:#666;font-size:0.8rem;margin-bottom:20px;">請輸入通關密碼</p>
            {% with msgs = get_flashed_messages() %}
                {% if msgs %}<p style="color:red;font-size:0.9rem;">{{ msgs[0] }}</p>{% endif %}
            {% endwith %}
            <form method="POST">
                <input type="password" name="password" autofocus placeholder="請輸入密碼" 
                       style="width:100%;padding:12px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;box-sizing:border-box;">
                <button type="submit" 
                        style="width:100%;padding:12px;background:#a0522d;color:white;border:none;border-radius:4px;cursor:pointer;font-weight:bold;">驗證識別</button>
            </form>
        </div>
    </body>
    </html>""")

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_list():
    fs = { k: get_files(v) for k, v in CATEGORIES.items() }
    return render_template('admin_list.html', files=fs)

@app.route('/admin/edit/<category>/<filename>')
@admin_required
def admin_edit(category, filename):
    target_dir = get_dir_by_category(category)
    if not target_dir: abort(404)
    filepath = safe_path(target_dir, filename)
    with open(filepath, 'r', encoding='utf-8-sig') as f: content = f.read()
    return render_template('admin_edit.html', category=category, filename=filename, content=content)

@app.route('/admin/save', methods=['POST'])
@admin_required
def admin_save():
    cat = request.form.get('category'); fn = request.form.get('filename'); cont = request.form.get('content', '')
    target_dir = get_dir_by_category(cat)
    if not target_dir or not fn: abort(400)
    filepath = safe_path(target_dir, fn)
    with open(filepath, 'w', encoding='utf-8') as f: f.write(cont)
    invalidate_cache(target_dir)
    return redirect(url_for('admin_list'))

@app.route('/admin/delete/<category>/<filename>', methods=['POST'])
@admin_required
def admin_delete(category, filename):
    target_dir = get_dir_by_category(category)
    filepath = safe_path(target_dir, filename)
    if os.path.exists(filepath): os.remove(filepath)
    invalidate_cache(target_dir)
    return redirect(url_for('admin_list'))

@app.route('/admin/upload', methods=['GET', 'POST'])
@admin_required
def admin_upload():
    if request.method == 'POST':
        title = request.form.get('title', 'Untitled'); category = request.form.get('category', 'work')
        desc = request.form.get('description', ''); file = request.files.get('file'); target_dir = get_dir_by_category(category)
        if not target_dir: abort(400)
        ts = int(time.time()); md_fn = f"{ts}.md"; content = desc
        if file and file.filename:
            f_name = secure_filename(file.filename); f_name = f"{ts}_{f_name}"
            file.save(os.path.join(target_dir, f_name)); ext = os.path.splitext(f_name)[1].lower()
            media_url = url_for('serve_entry_media', category=category, filename=f_name)
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']: content = f"![{title}]({media_url})\n\n" + content
            elif ext in ['.mp4', '.mov', '.webm']: content = f'<video controls style="width:100%"><source src="{media_url}"></video>\n\n' + content
        post = frontmatter.Post(content, title=title, date=datetime.now().strftime('%Y-%m-%d'))
        with open(os.path.join(target_dir, md_fn), 'wb') as f: frontmatter.dump(post, f)
        invalidate_cache(target_dir)
        return redirect(url_for('admin_list'))
    return render_template('admin_upload.html')

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(STATIC_IMAGES_DIR, filename)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close(); return ip
    except Exception: return "127.0.0.1"

if __name__ == '__main__':
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)
    except: pass
    
    local_ip = get_local_ip()
    port = 5000
    
    handler = logging.FileHandler(os.path.join(BASE_DIR, 'server.log'), encoding='utf-8')
    logger.addHandler(handler)
    
    print("\n" + "="*50)
    print("SUE LOG SERVER ACTIVE")
    print("-" * 50)
    print(f"LAPTOP: http://localhost:{port}")
    print(f"MOBILE: http://100.99.205.25:{port} (Tailscale)")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
