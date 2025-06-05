from _libs import *



@app.route('/')
def index():
    
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    db.close()

    if VULNERABLE:
        # Доверяем клиенту: он передаёт флаг через JS
        return render_template('posts.html', posts=posts, username='Anonymous (local)')
    
    if 'user_id' not in session:
        return redirect(url_for('login'))


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


