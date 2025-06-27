from flask import request, render_template, redirect, url_for, session, flash, send_file
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from icecream import ic
import bleach
import lxml.etree as ET  # Используем lxml для корректной демонстрации XXE
import io
import pickle
import json


@app.route('/')
def posts():
    db = get_db()
    # Получаем посты и количество комментариев к каждому
    posts = db.execute('''
        SELECT posts.*, 
               (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS comment_count
        FROM posts
    ''').fetchall()
    return render_template('posts.html', posts=posts, vulnerabilities=get_vuln_flag())


@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if not post:
        return 'No post', 404

    comments = db.execute('SELECT * FROM comments WHERE post_id=?', (post_id,)).fetchall()
    return render_template('post.html', post=post, comments=comments, vulnerabilities=get_vuln_flag())


@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'username' not in session:
        abort(403)

    author = session['username']
    content = request.form.get('content', '').strip()
    if not content:
        flash('Comment cannot be empty.')
        return redirect(url_for('post', post_id=post_id))

    flag = get_vuln_flag()  # твоя функция для получения текущей уязвимости

    import bleach
    safe_content = bleach.clean(
        content,
        tags=['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br'],
        attributes=['href']
    )

    db = get_db()
    db.execute(
        'INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)',
        (post_id, author, safe_content)
    )
    db.commit()
    flash('Comment added!')
    return redirect(url_for('post', post_id=post_id))

# for ssti via jinja2
def render_comment(content, flag=get_vuln_flag()):
    print(f"RENDER_SSTI: {content}, FLAG={flag}")

    if flag == 'ssti_jinja2':
        from flask import render_template_string
        try:
            return render_template_string(content)
        except Exception as e:
            return f"<span style='color:red'>SSTI error: {e}</span>"
    else:
        return content

app.jinja_env.globals.update(render_comment=render_comment)
# =========


@app.route('/preview_post/<int:post_id>')
def preview_post(post_id):
    print(f"SSRF preview: отправляю серверный запрос с User-Agent: {request.headers.get('User-Agent')}")
    flag = get_vuln_flag()
    if flag == 'blind_ssrf_shellshock':
        import requests
        try:
            # SSRF делает запрос во внутренний CGI endpoint, НЕ в сам app!
            r = requests.get("http://127.0.0.1:8080/cgi-bin/vuln", timeout=2, headers={
                'User-Agent': request.headers.get('User-Agent', 'BlogLabPreview')
            })
            print(f"Ответ от internal_api: {r.text}")
        except Exception as e:
            print(f"Ошибка SSRF: {e}")    # Показываем preview (можно просто страницу поста, или кусок)
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()

    return render_template('post_preview.html', post=post)


@app.route('/save_draft', methods=['POST'])
def save_draft():
    vuln = get_vuln_flag()
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if not title or not content:
        flash('Title and content required to save draft.')
        return redirect(url_for('post_creation'))

    draft = {
        'title': title,
        'content': content
    }
    if vuln == 'insecure_deserialization':
        buf = io.BytesIO()
        pickle.dump(draft, buf)
    else:
        buf = io.BytesIO(json.dumps(draft).encode())
    buf.seek(0)    

    return send_file(
        buf,
        as_attachment=True,
        download_name='post.draft',
        mimetype='application/octet-stream'
    )

@app.route('/post_creation', methods=['GET', 'POST'])
def post_creation():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db()
    vuln = get_vuln_flag()

    if request.method == 'POST':
        if 'draft_file' in request.files and request.files['draft_file'].filename:
            draft_data = request.files['draft_file'].read()
            try:
                if vuln == 'insecure_deserialization':
                    draft = pickle.loads(draft_data)
                else:
                    # В безопасном режиме поддерживаем только json-драфты
                    try:
                        draft = json.loads(draft_data)
                    except Exception:
                        flash('Only JSON drafts are supported in secure mode.')
                        return redirect(url_for('post_creation'))
                title = draft.get('title', 'Draft')
                content = draft.get('content', '')
            except Exception as e:
                flash('Ошибка загрузки черновика: ' + str(e))
                return redirect(url_for('post_creation'))

            author = session['username']
            db.execute(
                'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                (title, content, author)
            )
            db.commit()
            flash('Draft imported as post!')
            return redirect(url_for('post_creation'))
        else:
            # Обычное создание поста (через форму)
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            if not title or not content:
                flash('Title and content required.')
                return redirect(url_for('post_creation'))

            author = session['username']
            db.execute(
                'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                (title, content, author)
            )
            db.commit()
            flash('Post added!')
            return redirect(url_for('post_creation'))

    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('post_creation.html', posts=posts)
