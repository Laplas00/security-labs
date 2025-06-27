
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


import requests
from flask import send_file, abort
import io

@app.route('/avatar_proxy/<int:user_id>')
def avatar_proxy(user_id):
    db = get_db()
    row = db.execute('SELECT avatar_url FROM users WHERE id=?', (user_id,)).fetchone()
    if not row or not row['avatar_url']:
        return send_file('default_avatar.png', mimetype='image/png')

    avatar_url = row['avatar_url']
    vulnerability = get_vuln_flag()  # get_vuln_flag, не get_vuln_flags
    ssrf_flag = vulnerability == 'ssrf_whitelist_based_bypass'

    def is_url_ok(url):
        if ssrf_flag:
            return url.startswith('https://i.pravatar.cc')
        from urllib.parse import urlparse
        p = urlparse(url)
        return p.scheme == 'https' and p.hostname == 'i.pravatar.cc'

    if not is_url_ok(avatar_url):
        return send_file('default_avatar.png', mimetype='image/png')

    try:
        resp = requests.get(avatar_url, timeout=3)
        resp.raise_for_status()
        img_data = io.BytesIO(resp.content)
        mimetype = resp.headers.get('content-type')
        # fallback к jpeg если неизвестен mimetype
        return send_file(img_data, mimetype=mimetype or 'image/jpeg')
    except Exception:
        return send_file('default_avatar.png', mimetype='image/png')



def is_avatar_url_ok(url, vuln_flag):
    if vuln_flag == 'ssrf_whitelist_based_bypass':
        return url and url.startswith('https://i.pravatar.cc')
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        return (
            p.scheme == 'https' and
            p.hostname == 'i.pravatar.cc'
        )
    except Exception:
        return False



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

    if new_avatar_url and is_avatar_url_ok(new_avatar_url, vulnerability):
        db.execute(
            "UPDATE users SET username=?, avatar_url=? WHERE id=?",
            (new_username, new_avatar_url, user_id)
        )
        session['avatar_url'] = new_avatar_url
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

