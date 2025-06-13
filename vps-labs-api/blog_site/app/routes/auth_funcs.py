from flask import request, redirect, url_for, session, flash, render_template
import sqlite3
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flags
# login / logout / registration

# Realisation of vulnerables:
# SQL inj classic


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
        flags = get_vuln_flags()
        print('Login function is running')
        print('flags is:', flags)
        # === Уязвимость: SQL Injection (classic) ===
        if 'sql_inj_classic' in flags:
            print('this is sql_inj_classic module in auth')
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            user = db.execute(query).fetchone()
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Success! (SQLi)')
                return redirect(url_for('posts'))
            else:
                flash('Wrong username or password')
                return redirect(url_for('login'))

        # === Безопасная реализация ===
        user = db.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)).fetchone()
        print(user)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Success!')
            return redirect(url_for('posts'))
        else:
            flash('Wrong username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        flags = get_vuln_flags()

        # === Уязвимость: SQL Injection (classic) ===
        if 'sql_inj_classic' in flags:
            try:
                query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', 'user')"
                db.execute(query)
                db.commit()
                flash('Registration complete (SQLi), login!')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already in use')
                return render_template('register.html')

        # === Безопасная реализация ===
        try:
            db.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, password, 'user')
            )
            db.commit()
            flash('Registration complete, login!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already in use')
    return render_template('register.html')

