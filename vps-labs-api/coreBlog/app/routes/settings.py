
from flask import request, render_template, redirect, url_for, session, flash, abort
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag


# idor_bac

if get_vuln_flag() == 'circumbent_via_header':
    print('flag circumbent via header ')
    @app.before_request
    def circumbent_via_header():
        x_url = request.headers.get('X-Original-URL')
        if x_url == "/admin":
            # Выдаём контент "админки" (или любой другой секрет)
            return "<h1>⚠️ Access control bypassed via header!</h1><p>FLAG: circum_bypass</p>"



@app.route('/settings/users/<int:user_id>')
def settings(user_id):
    db = get_db()
    flag = get_vuln_flag()
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    show_admin_panel = False
    if not user:
        abort(404)
    
    match flag:
        case 'idor_bac':
            if str(user_id) == '1': 
                show_admin_panel = True
        
        case 'http_parameter_pollution_priv_esc':
            roles = request.args.getlist('role')  # e.g. ['user','admin']
            if len(roles) >= 2 and roles[-1] == 'admin':
                show_admin_panel = True
            else:
                show_admin_panel = user['role'] == 'admin'

        case 'dom_based_cookie_manipulation':
            is_admin_cookie = request.cookies.get("is_admin")
            if is_admin_cookie == "true":
                show_admin_panel = True
            else:
                show_admin_panel = user['role'] == 'admin'

    if not flag:
        if 'user_id' not in session or session['user_id'] != user_id:
            abort(403)
        show_admin_panel = user['role'] == 'admin'

    # Только если нужен admin panel, отправляем all_users
    all_users = db.execute("SELECT * FROM users").fetchall() if show_admin_panel else None

    return render_template(
        'settings.html',
        user=user,
        all_users=all_users,
        show_admin_panel=show_admin_panel,
        vulnerability=flag,
        session=session
    )


@app.route('/settings/users/<int:user_id>/update', methods=['POST'])
def update_settings(user_id):
    db = get_db()
    vulnerability = get_vuln_flag()
    new_username = request.form.get('username')

    if not new_username:
        flash('Username required')
        return redirect(url_for('settings', user_id=user_id))

    # === IDOR: любой может менять чужие настройки ===
    if vulnerability in ['idor_bac', 'http_parameter_pollution_priv_esc']:
        db.execute(
            "UPDATE users SET username=? WHERE id=?",
            (new_username, user_id)
        )

        # Обработка ролей (если есть админ-панель)
        all_users = db.execute("SELECT * FROM users").fetchall()
        for u in all_users:
            is_admin = f'is_admin_{u["id"]}' in request.form
            new_role = 'admin' if is_admin else 'user'
            db.execute(
                "UPDATE users SET role=? WHERE id=?",
                (new_role, u['id'])
            )
            # Если меняем текущего пользователя — обновим его роль в сессии
            if u['id'] == session.get('user_id'):
                session['role'] = new_role

        db.commit()
        flash('Settings updated! (IDOR enabled)')
        return redirect(url_for('settings', user_id=user_id))

    # === SAFE: только владелец аккаунта ===
    if 'user_id' not in session or session['user_id'] != user_id:
        abort(403)

    db.execute(
        "UPDATE users SET username=? WHERE id=?",
        (new_username,  user_id)
    )

    # Только админ может менять роли, и только свою страницу
    current_role = session.get('role')
    if current_role == 'admin':
        all_users = db.execute("SELECT * FROM users").fetchall()
        for u in all_users:
            is_admin = f'is_admin_{u["id"]}' in request.form
            new_role = 'admin' if is_admin else 'user'
            db.execute(
                "UPDATE users SET role=? WHERE id=?",
                (new_role, u['id'])
            )
            if u['id'] == session.get('user_id'):
                session['role'] = new_role

    db.commit()
    session['username'] = new_username
    flash('Settings updated!')
    return redirect(url_for('settings', user_id=user_id))

