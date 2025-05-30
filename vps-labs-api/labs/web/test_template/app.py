import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if not post:
        return 'No post', 404
    return render_template('post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Success!')
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Login success')
    return redirect(url_for('index'))

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
        flash('Пост добавлен!')
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('admin.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, 'user'))
            db.commit()
            flash('Registration complete, login!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already in use')
    return render_template('register.html')

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске
    app.run(host='0.0.0.0', port=8000) # for traefic use 5000

