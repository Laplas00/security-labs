from _libs import *



@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if not post:
        return 'No post', 404
    return render_template('post.html', post=post)


@app.route("/store_message", methods=["POST"])
def store_user_message():
    message = request.form.get("message", "").strip()
    vuln_mode = os.environ.get("VULNERABLE", "0") == "1"
    print('vuln mode in store messages:', vuln_mode)
    if False == vuln_mode:
        if "<script" in message.lower() or "</" in message.lower():
            flash("HTML tags are not allowed (vuln off).", "error")
            return redirect(url_for("discussion"))

    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO comments (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()
    flash("Message posted successfully!", "success")

    return redirect(url_for("discussion"))

@app.route("/discussion", methods=["GET"])
def discussion():
    vuln_mode = os.environ.get("VULNERABLE", "0") == "1"
    print('vuln_mode', vuln_mode)
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT message FROM comments ORDER BY id DESC LIMIT 50")
    comments = [row[0] for row in c.fetchall()]
    conn.close()

    return render_template(
        "discussion.html",
        comments=comments,
        vuln_mode=vuln_mode
    )
