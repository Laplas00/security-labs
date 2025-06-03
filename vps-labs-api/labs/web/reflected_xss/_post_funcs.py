from _libs import *



@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if not post:
        return 'No post', 404
    return render_template('post.html', post=post)


@app.route("/find-post", methods=["GET"])
def find_post():
    vuln_mode = VULNERABLE == '1'
    q = request.args.get("q", "")
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    # Поиск по всем полям (title, content, author)
    like_query = f"%{q}%"
    c.execute("SELECT title, content, author FROM posts WHERE title LIKE ? OR content LIKE ? OR author LIKE ?", 
              (like_query, like_query, like_query))
    posts = c.fetchall()
    conn.close()
    return render_template(
        "search_results.html", 
        q=q, 
        posts=posts, 
        vuln_mode=vuln_mode
    )

