
from flask import request, redirect, url_for, flash, render_template
from icecream import ic
from app.utils.vulns import get_vuln_flag

# ooooooooooooooooooooooooooooooooooooooooooooooo
# classic sql injection via login form (password don't required)
def sql_inj_classic(db, session, request):
    username = request.form['username']
    password = request.form['password']
    ic('this is sql_inj_classic module in auth')
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = db.execute(query).fetchone()
    ic(user)
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        flash('Success! (SQLi)')
        return redirect(url_for('posts'), )
    else:
        flash('Wrong username or password')
        return redirect(url_for('login'), )


# ooooooooooooooooooooooooooooooooooooooooooooooo
# imitate forgotten bypass code, that can be finded in cookies
def auth_bypass_forgotten_cookie(db, session, request):
    username = request.form['username']
    password = request.form['password']

    if request.cookies.get('debug_bypass') == '1':
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash("Auth bypassed via debug_bypass cookie!")
            resp = redirect(url_for('posts'), )
            # выставляем debug_bypass=0 всегда (видна в devtools)
            resp.set_cookie('debug_bypass', '0')
            return resp
    # обычная проверка
    user = db.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        flash("Logged in!")
        resp = redirect(url_for('posts'))
        resp.set_cookie('debug_bypass', '0')
        return resp
    flash("Invalid credentials")
    resp = redirect(url_for('login'))
    resp.set_cookie('debug_bypass', '0')
    return resp

# ooooooooooooooooooooooooooooooooooooooooooooooo
def bypass_2fa_weak_logic(db, session, request):
    username = request.form['username']
    password = request.form['password']

    user = db.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    ).fetchone()
    if user:
        session['pending_user'] = user['username']
        return redirect(url_for('login_verify'))
    else:
        flash('Wrong username or password')
        return redirect(url_for('login'))

def bypass_2fa_weak_logic_verification(db, session, request):
    pending_user = session.get('pending_user')
    if not pending_user:
        abort(403)

    if request.method == 'POST':
        input_code = request.form['verif_code']
        verify = request.form.get('verify', pending_user)
        user = db.execute("SELECT * FROM users WHERE username=?", (verify,)).fetchone()

        if user and user['verif_code'] == input_code:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session.pop('pending_user', None)
            flash("Login successful! (2FA bypassed)")
            return redirect(url_for('posts'))
        else:
            flash("Wrong verification code!")

    return render_template('code_verify.html', pending_user=pending_user, vulnerabilities=get_vuln_flag())

