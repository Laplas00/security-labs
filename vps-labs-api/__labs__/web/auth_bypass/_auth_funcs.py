from _libs import *

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout success')
    return redirect(url_for('index'))



@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json(force=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    db = get_db()
    print(username, password)
    if VULNERABLE:
        # уязвимая версия: всегда возвращаем false, чтобы студент мог подменить
        db.close()
        print('vulnerable version')
        return jsonify({"authenticated": False})

    # безопасная версия: параметризованный запрос
    user = db.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    ).fetchone()
    db.close()

    if user:
        # сохраняем сессию и возвращаем true
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})



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


