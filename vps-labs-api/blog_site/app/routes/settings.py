
from flask import request, render_template, redirect, url_for, session, flash, abort
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flags


# idor_bac


@app.route('/settings/users/<int:user_id>')
def settings(user_id):
    db = get_db()
    vulnerabilities = get_vuln_flags()

    if 'idor_bac' in vulnerabilities:
        # IDOR: любой может смотреть чужой профиль по id
        user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not user:
            abort(404)
        return render_template('settings.html', user=user, vulnerabilities=vulnerabilities)

    # SAFE: только владелец может смотреть свои настройки
    if 'user_id' not in session or session['user_id'] != user_id:
        abort(403)
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        abort(404)
    return render_template('settings.html', user=user, vulnerabilities=vulnerabilities)

@app.route('/settings/users/<int:user_id>/update', methods=['POST'])
def update_settings(user_id):
    db = get_db()
    vulnerabilities = get_vuln_flags()

    new_username = request.form.get('username')

    if not new_username:
        flash('Username required')
        return redirect(url_for('settings', user_id=user_id))

    # === Уязвимость: IDOR (Broken Access Control) ===
    if 'idor_bac' in vulnerabilities:
        # Любой пользователь может менять настройки любого пользователя по id
        db.execute(
            "UPDATE users SET username=? WHERE id=?",
            (new_username, user_id)
        )
        db.commit()
        flash('Settings updated! (IDOR enabled)')
        return redirect(url_for('settings', user_id=user_id))

    # === SAFE VARIANT ===
    # Только владелец аккаунта может менять свои настройки
    if 'user_id' not in session or session['user_id'] != user_id:
        abort(403)

    db.execute(
        "UPDATE users SET username=? WHERE id=?",
        (new_username,  user_id)
    )
    db.commit()
    session['username'] = new_username
    flash('Settings updated!')
    return redirect(url_for('settings', user_id=user_id))
