
from flask import request, render_template, redirect, url_for, session, flash, render_template_string
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag

@app.route("/find-post", methods=["GET"])
def find_post():
    q = request.args.get("q", "")
    flag = get_vuln_flag()
    conn = get_db()
    c = conn.cursor()
    
    # Безопасный режим
    like_query = f"%{q}%"
    c.execute(
        "SELECT id, title, content, author FROM posts WHERE title LIKE ? OR content LIKE ? OR author LIKE ?", 
        (like_query, like_query, like_query)
    )
    posts = c.fetchall()
    conn.close()
    # q подставляется как обычно — Jinja экранирует по умолчанию
    return render_template(
        "posts.html", 
        q=q,
        posts=posts,
        vulnerabilities=get_vuln_flag()
    )

