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
    print(4,request.cookies.get('session'))

    posts = db.execute('''
        SELECT posts.*, 
               (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS comment_count
        FROM posts
    ''').fetchall()
    return render_template('posts.html', posts=posts, vulnerability=get_vuln_flag())

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    print('someone got an request')
    print(post_id)
    flag = get_vuln_flag()
    if flag == 'basic_csrf':
        db = get_db()
        db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        db.commit()
        flash('Post deleted!')
        return redirect(url_for('posts', vulnerability=flag))
    else:
        try:
            if session['role'] == 'admin':
                ic('admin trying to delete post')
                db = get_db()
                db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
                db.commit()
                flash('Post deleted!')
                return redirect(url_for('posts', vulnerability=flag))
        except KeyError as e:
            print('haha ueban')
            return 'nuhai bebru'
   
    
@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if not post:
        return 'No post', 404

    comments = db.execute('SELECT * FROM comments WHERE post_id=?', (post_id,)).fetchall()
    return render_template('post.html', post=post, comments=comments, vulnerability=get_vuln_flag())


@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'username' not in session:
        abort(403)

    author = session['username']
    content = request.form.get('content', '').strip()
    if not content:
        flash('Comment cannot be empty.')
        return redirect(url_for('post', post_id=post_id))

    flag = get_vuln_flag()
    match flag:
        case 'stored_xss':
            safe_content = content 

        case 'clobbering_dom_attr_to_bp_html_filters':
            safe_content = content  # Без фильтрации — DOM clobbering

        case 'ssti_via_jinja2':
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

    if flag == 'ssti_via_jinja2':
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
    post_url = f"http://127.0.0.1:8000/post/{post_id}"  # Имитация внутреннего вызова
    if flag == 'blind_ssrf_shellshock':
        import requests
        try:
            # Здесь requests.get — это и есть твой SSRF. Pentester может подменить User-Agent.
            requests.get(post_url, timeout=2, headers={
                'User-Agent': request.headers.get('User-Agent', 'BlogLabPreview')
            })
        except Exception as e:
            pass
    # Показываем preview (можно просто страницу поста, или кусок)
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()

    return render_template('post_preview.html', post=post)



vulns_to_pass_user_create_post = [
        'dom_xss_polyglot',]

@app.route('/post_creation', methods=['GET', 'POST'])
def post_creation(): 
    flag = get_vuln_flag()

    if 'username' not in session:
        return redirect(url_for('login'), )

    if flag not in vulns_to_pass_user_create_post:
        if session.get('role') != 'admin':
            return redirect(url_for('login'), )

    db = get_db()


    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']

        # === Уязвимость: Stored XSS через посты ===
        if 'stored_xss_posts' in flag:
            # сохраняем без очистки
            db.execute(
                'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                (title, content, author)
            )
            db.commit()
            flash('Post added! (XSS enabled)')
            return redirect(url_for('post_creation'), )

        # === Безопасный вариант: экранируем вручную перед вставкой (если бы XSS был в title/content) ===
        # либо используем безопасный рендеринг в шаблоне через {{ }} без |safe

        db.execute(
            'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
            (title, content, author)
        )
        db.commit()
        flash('Post added!')
        return redirect(url_for('post_creation'))

    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('post_creation.html', posts=posts, vulnerability=flag)

