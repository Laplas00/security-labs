import io, time, os
from flask import send_file, request, render_template, redirect, url_for, session, flash, abort
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
import requests


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


@app.route('/avatar_proxy/<int:user_id>')
def avatar_proxy(user_id):
    db = get_db()
    row = db.execute('SELECT avatar_url FROM users WHERE id=?', (user_id,)).fetchone()
    if not row or not row['avatar_url']:
        return send_file('default_avatar.png', mimetype='image/png')

    avatar_url = row['avatar_url']
    vulnerability = get_vuln_flag()  # типа 'command_injection_basic' или None

    try:
        resp = requests.get(avatar_url, timeout=3)
        resp.raise_for_status()
        img_data = io.BytesIO(resp.content)
        mimetype = resp.headers.get('content-type')
        return send_file(img_data, mimetype=mimetype or 'image/jpeg')
    except Exception:
        return send_file('default_avatar.png', mimetype='image/png')

@app.route('/settings/users/<int:user_id>/update', methods=['POST'])
def update_settings(user_id):
    db = get_db()
    vulnerability = get_vuln_flag()
    new_username = request.form.get('username')
    new_avatar_url = request.form.get('avatar_url')

    if not new_username:
        flash('Username required')
        return redirect(url_for('settings', user_id=user_id))

    if 'user_id' not in session or session['user_id'] != user_id:
        abort(403)

    if new_avatar_url:
        db.execute(
            "UPDATE users SET username=?, avatar_url=? WHERE id=?",
            (new_username, new_avatar_url, user_id)
        )
        session['avatar_url'] = new_avatar_url
        db.commit()

        # ——— Vuln: only for the lab mode ———
        start = time.time()
        # unsafely interpolate URL
        os.system(f"python3 apply_avatar.py {user_id} {new_avatar_url}")
        delay = time.time() - start
        flash(f"⚡ Avatar updated! (took {delay:.2f}s)")

    else:
        db.execute(
            "UPDATE users SET username=? WHERE id=?",
            (new_username, user_id)
        )
        flash('Avatar URL not updated: only https://i.pravatar.cc/* allowed')

    db.commit()
    session['username'] = new_username
    flash('Settings updated!')
    return redirect(url_for('settings', user_id=user_id))

