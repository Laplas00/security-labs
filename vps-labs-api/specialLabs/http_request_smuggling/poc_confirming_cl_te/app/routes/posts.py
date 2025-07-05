from flask import request, render_template, redirect, url_for, session, flash
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from icecream import ic
import bleach
import time
from flask import current_app

last_post_html = None

@app.before_request
def smuggling_guard():
    global last_post_html
    # Считываем body как строку (RAW)
    raw = request.get_data(as_text=True)
    ic(dir(request))
    ic(request.args)
    ic(request.data)

    ic(request.get_data())
    ic(request.values)
    ic(request.view_args)
    ic(request.want_form_data_parsed)


    print('-----')

    ic(raw)
    ic(request)
    # Пример: ловим "GET /hacked" внутри body
    shared_flag = current_app.config['shared_flag']
    if shared_flag["cl_te"]:        
        last_post_html = "✅ CL.TE Smuggling Triggered!"


@app.route('/last_post', methods=['GET', 'POST'])
def last_post():
    global last_post_html
    xfh = request.headers.get('X-Forwarded-Host')
    if request.method == 'POST' and xfh:
        html = f"<h1>hacked: {xfh}</h1>"
        last_post_html = html
    if last_post_html:
        return last_post_html
    return "Нет постов."

@app.route('/')
def posts():
    global last_post_html
    db = get_db()
    # Получаем посты и количество комментариев к каждому
    posts = db.execute('''
        SELECT posts.*, 
               (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS comment_count
        FROM posts
    ''').fetchall()

    return render_template('posts.html', posts=posts, vulnerabilities=get_vuln_flag(), last_post=last_post)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    global last_post_html
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    ic(post)
    if not post:
        return 'No post', 404

    ic(post_id)

    comments = db.execute('SELECT * FROM comments WHERE post_id=?', (post_id,)).fetchall()
    # Рендерим HTML
    html = render_template('post.html', post=post, comments=comments)
    # Сохраняем для "last_post"
    last_post_html = html
    return html

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

    match flag:
        case 'clobbering_dom_attr_to_bp_html_filters':
            safe_content = content  # Без фильтрации — DOM clobbering

        case 'ssti_jinja2':
            # Сохраняем как есть, но на этапе вывода подставляем render_template_string
            safe_content = content

        case _:
            # Безопасный режим — чистим всё опасное
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





@app.route('/post_creation', methods=['GET', 'POST'])
def post_creation():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    vuln = get_vuln_flag()

    if request.method == 'POST':
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
