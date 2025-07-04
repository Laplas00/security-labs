
from flask import request, redirect, url_for, flash, flash, render_template_string

from icecream import ic
from app.utils.app import get_db


# connection(db), cursor
def reflected_xss(q):
    print("Query", q)
    conn = get_db()
    c = conn.cursor()

    like_query = f"%{q}%"
    c.execute(
        "SELECT id, title, content, author FROM posts WHERE title LIKE ? OR content LIKE ? OR author LIKE ?", 
        (like_query, like_query, like_query)
    )
    posts = c.fetchall()
    # ВНИМАНИЕ: q инъецируется напрямую (без экранирования!)
    
    return render_template_string(
        """
        {% extends "base.html" %}
        {% block content %}
        <h2>Результаты поиска для: {{ q|safe }}</h2>
        <div class="feed-container">
        <p>--------------------------</p>
          {% for post in posts %}
            <div class="post-card">
              <div class="post-card__info">
                <div class="post-card__meta">
                  <span class="post-card__author">{{ post.author }}</span>
                  <span class="post-card__date">{{ post.date or '' }}</span>
                  <span class="post-card__comments">💬 {{ post.comment_count }} comments</span>
                </div>
                <a href="{{ url_for('post', post_id=post['id']) }}" class="post-card__title">
                  {{ post.title }}
                </a>
                <div class="post-card__subtitle">{{ post.subtitle or post.content[:128] ~ "..." }}</div>
              </div>
            </div>
          {% endfor %}
        </div>
        {% endblock %}
        """,
        q=q,
        posts=posts
    )


