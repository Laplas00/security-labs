from _libs import *


@app.route('/')
def index():
    return render_template('login.html')

@app.route("/posts")
def posts():
    """
    Protected page. 
    - Vulnerable mode: require only pre_2fa_user (login step), then trust finalize-login to set user_id.
    - Secure mode: require session["user_id"] (i.e. full auth + 2FA).
    """
    if VULNERABLE == "0":
        if "user_id" not in session:
            return redirect(url_for("login"))
    else:
        if "pre_2fa_user" not in session and "user_id" not in session:
            # If neither step is done, redirect to login
            return redirect(url_for("login"))
        # Note: we do NOT require "user_id" here if vulnerable,
        # because the student will call /finalize-login to set it.

    db = get_db()
    rows = db.execute("SELECT id, title, content, author FROM posts").fetchall()
    db.close()
    all_posts = [dict(row) for row in rows]
    ic(all_posts)
    return render_template("posts.html", posts=all_posts) 

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


