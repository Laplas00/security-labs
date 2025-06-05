from _libs import *

@app.route('/')
def index():
    if not VULNERABLE:
        if 'user_id' not in session:
            return redirect(url_for('login'))

    # В уязвимом режиме не проверяем (позволяем попасть, если студент подменил JSON и JS сделал redirect)
    user_name = session.get('username')
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('posts.html', posts=posts, username=user_name)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        db.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)', (title, content, author))
        db.commit()
        flash('Post added!')
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('admin.html', posts=posts)


