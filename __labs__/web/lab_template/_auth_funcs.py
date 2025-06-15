from _libs import *

@app.route('/logout')
def logout():
    session.clear()
    flash('Login success')
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        if VULNERABLE:
            # Уязвимый SQL: прямое включение данных пользователя (SQL Injection)
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            user = db.execute(query).fetchone()
        else:
            # Безопасный SQL: параметризация
            user = db.execute(
                'SELECT * FROM users WHERE username=? AND password=?',
                (username, password)
            ).fetchone()

        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Success!')
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password')
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


