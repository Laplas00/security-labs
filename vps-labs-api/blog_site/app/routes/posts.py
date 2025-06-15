from flask import request, render_template, redirect, url_for, session, flash
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from icecream import ic
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

    db = get_db()
    db.execute('INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)',
               (post_id, author, content))
    db.commit()
    flash('Comment added!')
    return redirect(url_for('post', post_id=post_id))

@app.route('/post_creation', methods=['GET', 'POST'])
def post_creation():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'), )

    db = get_db()
    flags = get_vuln_flag()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']

        # === Уязвимость: Stored XSS через посты ===
        if 'stored_xss_posts' in flags:
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
    return render_template('post_creation.html', posts=posts)

