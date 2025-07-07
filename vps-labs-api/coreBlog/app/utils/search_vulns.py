
from flask import request, redirect, url_for, flash, flash, render_template_string
from werkzeug.routing import BuildError
from icecream import ic
from app.utils.app import get_db
from time import time, sleep



def blind_sql_injection_time_delay(request):
    def time_to_sleep(n):
        print('time to sleep')
        sleep(n) 

    print('function runned!!')
    term = request.args.get('q', '')
    start = time()
    conn = get_db()
    conn.create_function("sleep", 1, time_to_sleep)

        # VULNERABLE: directly interpolating user input into SQL
    sql = f"SELECT id, title, content FROM posts WHERE title LIKE '%{term}%'"
    try:
        rows = conn.execute(sql).fetchall()
        print('no error')

    except Exception as e:
        print('Exception:', e)
        flash(str(e))

    elapsed = time() - start
    flash(f'Search time: {elapsed}')
    
    try: 
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
            q=term,
            posts=rows)

    except BuildError:
        flash('Build error')
        return redirect(url_for('posts'))

    except Exception as e:
        flash('Error occured')
        return redirect(url_for('posts'))

def sql_union_column_number_discovery(requets):
    rows = []
    term = request.args.get('q', '')
    # VULNERABLE: directly interpolating user input into SQL
    sql = f"SELECT id, title, content FROM posts WHERE title LIKE '%{term}%'"
    try:
        rows = get_db().execute(sql).fetchall()
        print('no error')

    except Exception as e:
        print('Exception:', e)
        flash(str(e))
    
    try: 
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
            q=term,
            posts=rows)
    except BuildError:
        flash('You found out the correct numbers of columns')
        return redirect(url_for('posts'))

    except Exception as e:
        flash('You found out the correct numbers of columns')
        return redirect(url_for('posts'))




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


