import os

INDEX_PATH = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\templates\index.html"
STATIC_IMAGES_DIR = r"c:\Users\user\.gemini\antigravity\brain\My_AI_Project\sue_life_work_log\static\images"

SCENES = {
    "work": "work_scene_watercolor.svg",
    "life": "life_scene_watercolor.svg",
    "videos": "videos_scene_watercolor.svg",
    "podcasts": "podcasts_scene_watercolor.svg"
}

new_index = r'''{% extends "base.html" %}

{% block content %}
<div class="header-section" style="display:none;" style="text-align: center; margin-bottom: 60px;">
    <h1>{{ title or "Sue's Life & Work Log" }}</h1>
    <p class="subtitle" style="font-size: 1.2rem; color: var(--text-muted); font-style: italic;">Capturing the moments
        of life and the progress of work</p>
</div>

{# Work Section #}
<div class="category-section">
    <div class="section-header">
        <h2>Work Journal</h2>
        <a href="/work" class="see-all">VIEW ALL</a>
    </div>
    <div class="scene-illustration" style="width: 100%; max-height: 220px; overflow: hidden; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <img src="{{ url_for('static', filename='images/work_scene_watercolor.svg') }}" alt="Work Scene" style="width: 100%; height: auto; display: block;">
    </div>

    {% if work %}
    <ul class="entry-list">
        {% for post in work %}
        <li class="entry-item">
            <span class="entry-date">{{ post.date }}</span>
            <h3 class="entry-title"><a href="/entry/work/{{ post.filename }}">{{ post.title }}</a></h3>
            <div class="entry-summary">
                {{ post.content[:120] | striptags }}...
            </div>
            <a href="/entry/work/{{ post.filename }}" class="btn"
                style="align-self: flex-start; margin-top: auto; padding: 8px 16px; font-size: 0.85rem;">Read More</a>
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p style="color: var(--text-muted); font-style: italic;">No work entries yet.</p>
    {% endif %}
</div>

{# Life: Me #}
<div class="category-section">
    <div class="section-header">
        <h2>Life: My Stories</h2>
        <a href="/life/daily/me" class="see-all">VIEW ALL</a>
    </div>
    <div class="scene-illustration" style="width: 100%; max-height: 220px; overflow: hidden; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <img src="{{ url_for('static', filename='images/life_scene_watercolor.svg') }}" alt="Life Scene" style="width: 100%; height: auto; display: block;">
    </div>

    {% if daily_me %}
    <ul class="entry-list">
        {% for post in daily_me %}
        <li class="entry-item">
            <span class="entry-date">{{ post.date }}</span>
            <h3 class="entry-title"><a href="/entry/life_daily_me/{{ post.filename }}">{{ post.title }}</a></h3>
            <div class="entry-summary">
                {{ post.content[:120] | striptags }}...
            </div>
            <a href="/entry/life_daily_me/{{ post.filename }}" class="btn"
                style="align-self: flex-start; margin-top: auto; padding: 8px 16px; font-size: 0.85rem;">Read More</a>
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p style="color: var(--text-muted); font-style: italic;">No personal stories yet.</p>
    {% endif %}
</div>

{# Life: Travel #}
{% if travel %}
<div class="category-section">
    <div class="section-header">
        <h2>Travel Adventures</h2>
        <a href="/life/travel" class="see-all">VIEW ALL</a>
    </div>
    <div class="scene-illustration" style="width: 100%; max-height: 220px; overflow: hidden; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <img src="{{ url_for('static', filename='images/life_scene_watercolor.svg') }}" alt="Travel Scene" style="width: 100%; height: auto; display: block;">
    </div>

    <ul class="entry-list">
        {% for post in travel %}
        <li class="entry-item">
            <span class="entry-date">{{ post.date }}</span>
            <h3 class="entry-title"><a href="/entry/life_travel/{{ post.filename }}">{{ post.title }}</a></h3>
            <a href="/entry/life_travel/{{ post.filename }}" class="btn"
                style="align-self: flex-start; margin-top: 15px; padding: 8px 16px; font-size: 0.85rem;">Read
                Adventure</a>
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}

{# Videos #}
{% if videos %}
<div class="category-section">
    <div class="section-header">
        <h2>Video Projects</h2>
        <a href="/videos" class="see-all">VIEW ALL</a>
    </div>
    <div class="scene-illustration" style="width: 100%; max-height: 220px; overflow: hidden; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <img src="{{ url_for('static', filename='images/videos_scene_watercolor.svg') }}" alt="Videos Scene" style="width: 100%; height: auto; display: block;">
    </div>

    <ul class="entry-list">
        {% for post in videos %}
        <li class="entry-item">
            <span class="entry-date">{{ post.date }}</span>
            <h3 class="entry-title"><a href="/entry/videos/{{ post.filename }}">{{ post.title }}</a></h3>
            <a href="/entry/videos/{{ post.filename }}" class="btn"
                style="align-self: flex-start; margin-top: 15px; padding: 8px 16px; font-size: 0.85rem;">Watch Video</a>
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}

{# Podcasts #}
{% if podcasts %}
<div class="category-section">
    <div class="section-header">
        <h2>Podcasts</h2>
        <a href="/podcasts" class="see-all">VIEW ALL</a>
    </div>
    <div class="scene-illustration" style="width: 100%; max-height: 220px; overflow: hidden; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <img src="{{ url_for('static', filename='images/podcasts_scene_watercolor.svg') }}" alt="Podcasts Scene" style="width: 100%; height: auto; display: block;">
    </div>

    <ul class="entry-list">
        {% for post in podcasts %}
        <li class="entry-item">
            <span class="entry-date">{{ post.date }}</span>
            <h3 class="entry-title"><a href="/entry/podcasts/{{ post.filename }}">{{ post.title }}</a></h3>
            <a href="/entry/podcasts/{{ post.filename }}" class="btn"
                style="align-self: flex-start; margin-top: 15px; padding: 8px 16px; font-size: 0.85rem;">Listen</a>
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}
{% endblock %}
'''

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(new_index)

print("index.html rewritten with full-width scene illustrations.")
