from flask import request, redirect, url_for, session, flash, render_template, abort
import sqlite3
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from app.utils.auth_vulns import sql_inj_classic
from icecream import ic
import random
# login / logout / registration

# Realisation of vulnerables:
# SQL inj classic

if get_vuln_flag() == 'front_end_request_rewriting':
    ic('flag request_rewriting via header ')
    @app.before_request
    def front_end_request_rewriting():
        ic('function front_end_request_rewriting runned')
        x_url = request.headers.get('X-Original-URL')
        if x_url == "/admin":
            print('flag request_rewriting via header')
            return (
                "<h1>⚠️ Access control bypassed via header!</h1>"
                "<p>FLAG: request_rewriting via header</p>"
            )


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout success')
    return redirect(url_for('posts'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        flag = get_vuln_flag()
        ic('Login function is running')
        ic(flag)

        match flag:
            case 'sql_inj_classic':
                return sql_inj_classic(db, session, request)

            case 'auth_bypass_forgotten_cookie':
                return auth_bypass_forgotten_cookie(db, session, request)
                
            case '2fa_bypass_weak_logic':
                return bypass_2fa_weak_logic(db, session, request)

        # === Безопасная реализация (с обязательным 2FA) ===
        user = db.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)).fetchone()
        if user:
            session['pending_user'] = user['username']
            return redirect(url_for('login_verify'))
        else:
            flash('Wrong username or password')
            return redirect(url_for('login'))

    return render_template('login.html',vulnerabilities=get_vuln_flag())


@app.route('/login/verify', methods=['GET', 'POST'])
def login_verify():
    db = get_db()
    flag = get_vuln_flag()
    match flag:
        case '2fa_bypass_weak_logic':
            return bypass_2fa_weak_logic_verification(db, session, request)

    # --- Безопасная логика ---
    pending_user = session.get('pending_user')
    if not pending_user:
        abort(403)
    if request.method == 'POST':
        input_code = request.form['verif_code']
        user = db.execute("SELECT * FROM users WHERE username=?", (pending_user,)).fetchone()

        if user and user['verif_code'] == input_code:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session.pop('pending_user', None)
            flash("Login successful!")
            return redirect(url_for('posts'))
        else:
            flash("Wrong verification code!")
    return render_template('code_verify.html', pending_user=pending_user, vulnerabilities=get_vuln_flag())


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Сгенерировать verif_code
        verif_code = '0000'

        # Сохраняем юзера с кодом
        db.execute(
            "INSERT INTO users (username, password, email, verif_code, role) VALUES (?, ?, ?, ?, ?)",
            (username, password, email, verif_code, 'user')
        )
        db.commit()
        flash(f"Ваш код подтверждения: {verif_code}")  # Показываем код пользователю (как будто email)
        return redirect(url_for('verify_register', username=username, vulnerabilities=get_vuln_flag()))
    return render_template('register.html')

@app.route('/register/verify', methods=['GET', 'POST'])
def verify_register():
    db = get_db()
    username = request.args.get('username')
    if request.method == 'POST':
        input_code = request.form['verif_code']
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and user['verif_code'] == input_code:
            # здесь можно добавить поле "is_active" в БД и поставить его в 1, если хочешь сделать прям как в жизни
            flash("Регистрация завершена!")
            return redirect(url_for('login'))
        flash("Неверный код!")
    return render_template('code_verify.html', username=username)

