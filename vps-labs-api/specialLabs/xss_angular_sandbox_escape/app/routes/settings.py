
from flask import request, render_template, redirect, url_for, session, flash, abort
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag


# idor_bac




@app.route('/settings/users/<int:user_id>')
def settings(user_id):
    db = get_db()
    flag = get_vuln_flag()
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        abort(404)
    
    # safe
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
        vulnerabilities=flag,
        session=session
    )


@app.route('/settings/users/<int:user_id>/update', methods=['POST'])
def update_settings(user_id):
    db = get_db()
    vulnerabilities = get_vuln_flags()
    new_username = request.form.get('username')

    if not new_username:
        flash('Username required')
        return redirect(url_for('settings', user_id=user_id))

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

