
from flask import request, render_template, redirect, url_for, session, flash
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flags

@app.route("/find-post", methods=["GET"])
def find_post():
    q = request.args.get("q", "")
    flags = get_vuln_flags()
    conn = get_db()
    c = conn.cursor()

    # === Уязвимость: SQL Injection через поисковую строку ===
    if 'sql_inj_search' in flags:
        # Вставка q напрямую (НЕ безопасно!)
        query = f"SELECT title, content, author FROM posts WHERE title LIKE '%{q}%' OR content LIKE '%{q}%' OR author LIKE '%{q}%'"
        c.execute(query)
        posts = c.fetchall()
        conn.close()
        return render_template(
            "search_results.html", 
            q=q,
            posts=posts,
            vuln_mode='sql_inj_search'
        )

    # === SAFE VARIANT ===
    like_query = f"%{q}%"
    c.execute(
        "SELECT * FROM posts WHERE title LIKE ? OR content LIKE ? OR author LIKE ?", 
        (like_query, like_query, like_query)
    )
    posts = c.fetchall()
    conn.close()
    return render_template(
        "posts.html", 
        q=q,
        posts=posts,
        vuln_mode='safe'
    )

