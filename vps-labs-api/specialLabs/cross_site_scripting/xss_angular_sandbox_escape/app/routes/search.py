
from flask import request, render_template, redirect, url_for, session, flash, render_template_string
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from app.utils.search_vulns import reflected_xss, reflected_xss_angularjs_sandbox_escape


@app.route("/find-post", methods=["GET"])
def find_post():
    q = request.args.get("q", "")
    print(q)
    flag = get_vuln_flag()
    print(flag)

    conn = get_db()
    c = conn.cursor()
    like_query = f"%{q}%"
    c.execute(
        "SELECT id, title, content, author FROM posts WHERE title LIKE ? OR content LIKE ? OR author LIKE ?", 
        (like_query, like_query, like_query)
    )
    posts = c.fetchall()
    conn.close()
    # ВСЕГДА возвращаем posts
    return render_template(
        "posts.html", 
        q=q,
        posts=posts,
        vulnerability=flag
    )

