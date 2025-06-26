from flask import request, redirect, url_for, session, flash, render_template, abort, g
import sqlite3
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from app.utils.auth_vulns import sql_inj_classic
from icecream import ic
import random
import uuid



@app.before_request
def verify_or_create_session():
    db = get_db()
    session_id = request.args.get('session_id')

    # 1) Если session_id нет — создаём гостевую сессию и редиректим
    if not session_id:
        session_id = str(uuid.uuid4())
        db.execute(
            'INSERT INTO sessions (session_id) VALUES (?)',
            (session_id,)
        )
        db.commit()
        return redirect(url_for(request.endpoint,
                                session_id=session_id,
                                **(request.view_args or {})))

    # 2) Если session_id есть, но не в базе — заново создаём запись и редиректим
    session_data = db.execute(
        'SELECT user_id FROM sessions WHERE session_id = ?',
        (session_id,)
    ).fetchone()
    if not session_data:
        db.execute(
            'INSERT INTO sessions (session_id) VALUES (?)',
            (session_id,)
        )
        db.commit()
        return redirect(url_for(request.endpoint,
                                session_id=session_id,
                                **(request.view_args or {})))

    # 3) Session найдена — сохраняем в g и подтягиваем username (если залогинен)
    g.session_id = session_id
    g.user_id = session_data['user_id']
    if g.user_id:
        user = db.execute(
            'SELECT username FROM users WHERE id = ?',
            (g.user_id,)
        ).fetchone()
        g.username = user['username']
    else:
        g.username = None

    # 4) «Оживляем» Flask-session, чтобы в шаблонах session.username работал
    if g.username:
        session['username'] = g.username
        session['user_id']   = g.user_id
    else:
        session.pop('username', None)
        session.pop('user_id',   None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db   = get_db()
    flag = get_vuln_flag()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()

        if user:
            if flag != 'session_fixation':
                new_id = str(uuid.uuid4())
                db.execute(
                    'UPDATE sessions SET session_id = ? WHERE session_id = ?',
                    (new_id, g.session_id)
                )
                db.commit()
                g.session_id = new_id

            # 1) Привязываем user_id к этой session_id в БД
            db.execute(
                'UPDATE sessions SET user_id = ? WHERE session_id = ?',
                (user['id'], g.session_id)
            )
            db.commit()

            # 2) Дублируем в Flask-session для шаблонов
            session['username'] = user['username']
            session['user_id']  = user['id']

            flash('Hello, ' + user['username'] + '!')
            return redirect(url_for('posts', session_id=g.session_id))
        else:
            flash('Wrong username or password')
            return redirect(url_for('login', session_id=g.session_id))

    # GET
    return render_template(
        'login.html',
        vulnerabilities = flag,
        session_id      = g.session_id
    )

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout success')
    return redirect(url_for('posts'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        verif_code = '0000'
        # Сохраняем юзера с кодом
        db.execute(
            "INSERT INTO users (username, password, email, verif_code, role) VALUES (?, ?, ?, ?, ?)",
            (username, password, email, verif_code, 'user')
        )
        db.commit()
        return redirect(url_for('login', session_id=g.session_id))
    return render_template('register.html', session_id=g.session_id)
   


