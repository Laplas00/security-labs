from flask import request, render_template, redirect, url_for, session, flash
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from icecream import ic
import bleach

# posts / post_creation


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
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()

    return render_template('post_preview.html', post=post)




from flask import request, session, redirect, url_for, flash, render_template
import lxml.etree as ET  # Используем lxml для корректной демонстрации XXE

@app.route('/post_creation', methods=['GET', 'POST'])
def post_creation():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db()
    vuln = get_vuln_flag()

    if request.method == 'POST':
        if 'xml_file' in request.files and request.files['xml_file'].filename:
            xml_data = request.files['xml_file'].read()
            try: 
                parser = ET.XMLParser(load_dtd=True, resolve_entities=True)
                # Parse
                root = ET.fromstring(xml_data, parser)

                # Extract fields
                title     = root.findtext('title')
                body_text = root.findtext('body')

                _ = int(body_text)

                content = body_text

            except Exception as e:
                flash('Error while loading: ' + str(e))
                return redirect(url_for('post_creation'))        
        else:
            title = request.form['title']
            content = request.form['content']

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
