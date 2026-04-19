from datetime import datetime
from werkzeug.utils import secure_filename
import os, frontmatter, markdown, mimetypes
from flask import Flask, render_template, render_template_string, abort, request, redirect, url_for, send_from_directory, session
from functools import wraps

app = Flask(__mame__)
app.secret_key = 'sue2026'
ADMIN_PASSWORD = 'sue2026'

def admin_required(f):
    @wraps(f)
    def dec(*a, *
k):
        if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
        return f(*a, *
k)
    return dec

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
OS_DIRS = [
    os.path.join(CONTENT_DIR, 'work'),
    os.path.join(CONTENT_DIR, 'life', 'travel'),
    os.path.join(CONTENT_DIR, 'life', 'daily', 'me'),
    os.path.join(CONTENT_DIR, 'life', 'daily', 'grandma'),
    os.path.join(CONTENT_DIR, 'videos'),
    os.path.join(CONTENT_DIR, 'podcasts'),
    os.path.join(BASE_DIR, 'static', 'images')
]*for d in OS_DIRS: os.makedirs(d, exist_ok=True)

def get_files(d):
    fls = []
    if not os.path.exists(d): return fls
    for fn in os.listdir(d):
        if fn.endswith('.md'):
            try:
                with open(os.path.join(d, fn(¤°€Èœ°•¹½‘¥¹œôÕÑ˜´àµÍ¥œœ¤…Ì˜è(€€€€€€€€€€€€€€€€€€€À€ô™É½¹Ñµ…ÑÑ•È¹±½…¡˜¤(€€€€€€€€€€€€€€€€€€€™±Ì¹…ÁÁ•¹¡ì™¥±•¹…¹–œè™¹ˆ°€‘…Ñ”œèÀ¹•Ğ ‘…Ñ”œ¤°€Ñ¥Ñ±”œèÀ¹•Ğ Ñ¥Ñ±”œ¤½È™¹ˆ°€½¹Ñ•¹Ğœèµ…É­‘½İ¸¹µ…É­‘½İ¸¡À¹½¹Ñ•¹Ğ¥ô¤(€€€€€€€€€€€•á•ÁĞèÁ…ÍÌ(€€€™±Ì¹Í½ÉĞ¡­•äõ±…µ‰‘„àèÍÑÈ¡ál‘…Ñ”t¤°É•Ù•ÉÍ”õQÉÕ”¤(€€€É•ÑÕÉ¸™±Ì()‘•˜‘¥È¡Œ¤è(€€€€ôì(€€€€€€€€İ½É¬œè½Ì¹Á…Ñ ¹©½¥¸¡=9Q9Q}%H°€İ½É¬œ¤°(€€€€€€€€±¥™•}ÑÉ…Ù•°œè½Ì¹Á…Ñ ¹©½¥¸¡=9Q9Q}%H°€±¥™”œ°€ÑÉ…Ù•°œ¤°(€€€€€€€€€±¥™•}‘…¥±å}µ”œè½Ì¹Á…Ñ ¹©½¥¸¡=9Q9Q}%H°€ìife', 'daily', 'me'),
         'life_daily_grandma': os.path.join(CONTENT_DIR, 'life', 'daily', 'grandma'),
        'videos': os.path.join(CONTENT_DIR, "videos"),
         'podcasts': os.path.join(CONTENT_DIR, "podcasts")
    }
    return d.get(c)

@app.route('/')
def index():
    return render_template('index.html', work=get_files(gdir('work')), daily_me=get_files(gdir('life_daily_me')))

@app.route('/admin')
@admin_required
def admin_list():
    fs = {k: get_files(gdir(k)) for k in ['work', 'life_travel', 'life_daily_me', 'life_daily_grandma', 'videos', 'podcasts']}
    return render_template('admin_list.html', files=fs)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_list'))
    return render_template_string(''')

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)
