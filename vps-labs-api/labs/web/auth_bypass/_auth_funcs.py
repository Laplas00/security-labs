from _libs import *

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout success')
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    # --- Если пришёл AJAX‐запрос (JSON) ---
    if request.method == 'POST' and request.is_json:
        print('request post and request is json')
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        db = get_db()
        # В уязвимом режиме мы ОБЯЗАТЕЛЬНО возвращаем authenticated=False
        if VULNERABLE:
            db.close()
            flash('vuln is on, try to bypass me')
            return jsonify({"authenticated": False})

        # В “закрытом” режиме проверяем через параметризацию
        user = db.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        ).fetchone()
        db.close()

        if user:
            # Сохраняем session и возвращаем success
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login success')
            return jsonify({"authenticated": True})
        else:
            flash('Error occured')
            return jsonify({"authenticated": False})

    # --- GET → отрисовываем обычную форму с JS ---
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        if VULNERABLE:
            # Уязвимый SQL: прямое включение данных пользователя
            try:
                query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', 'user')"
                db.execute(query)
                db.commit()
                flash('Registration complete, login!')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already in use')
        else:
            # Безопасная регистрация
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


