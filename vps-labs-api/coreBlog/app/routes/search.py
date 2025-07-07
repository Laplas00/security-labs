
from flask import request, render_template, redirect, url_for, session 
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from app.utils.search_vulns import reflected_xss, sql_union_column_number_discovery

@app.route("/find-post", methods=["GET"])
def find_post():
    q = request.args.get("q", "")
    flag = get_vuln_flag()
    conn = get_db()
    c = conn.cursor()
    
    match flag:
        case 'reflected_xss':
            print('reflected xss')
            return reflected_xss(q)

        case 'reflected_xss_angularjs_sandbox_escape': 
            print('reflected xss angularjs sandbox escape (front vuln)')
            q = request.args.get("q", "")
            return render_template(
                "posts.html",
                q=q,
                vulnerabilities=get_vuln_flag())

        case 'sql_union_column_number_discovery':
            print('sql_union_column_number_discovery | Match case')
            return sql_union_column_number_discovery(request)

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

