from _libs import *



@app.route('/')
def index():
    if VULNERABLE:
        # В уязвимом режиме просто рендерим страницу с постами, 
        # не проверяем session и ничего не редиректим.
        db = get_db()
        posts = db.execute('SELECT * FROM posts').fetchall()
        db.close()
        return render_template('posts.html', posts=posts, username="Anonymous (bypassed)")
    
    # В безопасном режиме, как обычно, проверяем сессию:
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    db.close()
    return render_template('posts.html', posts=posts, username=session.get('username'))



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


