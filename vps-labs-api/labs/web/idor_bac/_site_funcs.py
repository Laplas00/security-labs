from _libs import *


@app.route('/')
def posts():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('posts.html', posts=posts)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        db.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)', (title, content, author))
        db.commit()
        flash('Post added!')
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('admin.html', posts=posts)




@app.route('/settings/users/<int:user_id>')
def settings(user_id):
    db = get_db()

    if VULNERABLE:
        # Просто берём пользователя по переданному user_id
        user = db.execute(
            'SELECT id, username, role FROM users WHERE id = ?;',
            (user_id,)
        ).fetchone()
        if not user:
            db.close()
            return "User not found", 404

        # Если роль у этого user_id == 'admin', показываем панель админа
        if user['role'] == 'admin':
            all_users = db.execute(
                'SELECT id, username, role FROM users;'
            ).fetchall()
            db.close()
            return render_template(
                'settings.html',
                vulnerable=True,
                is_admin=True,
                user_id=user['id'],
                username=user['username'],
                role=user['role'],
                all_users=all_users
            )
        else:
            # Обычный пользователь, показываем только форму с username
            db.close()
            return render_template(
                'settings.html',
                vulnerable=True,
                is_admin=False,
                user_id=user['id'],
                username=user['username'],
                role=user['role'],
                all_users=None
            )

    # === ЗАЩИЩЁННАЯ ВЕРСИЯ ===
    if 'user_id' not in session:
        db.close()
        return redirect(url_for('login'))

    current_id   = session['user_id']
    current_role = session.get('role', '')

    # Обычный пользователь не может смотреть чужие настройки
    if current_id != user_id and current_role != 'admin':
        db.close()
        return "Access Denied", 403

    # Берём запись целевого пользователя
    user = db.execute(
        'SELECT id, username, role FROM users WHERE id = ?;',
        (user_id,)
    ).fetchone()
    if not user:
        db.close()
        return "User not found", 404

    # Если текущий админ, даём список всех юзеров
    all_users = None
    if current_role == 'admin':
        all_users = db.execute(
            'SELECT id, username, role FROM users;'
        ).fetchall()

    db.close()
    return render_template(
        'settings.html',
        vulnerable=False,
        is_admin=(current_role == 'admin'),
        user_id=user['id'],
        username=user['username'],
        role=user['role'],
        all_users=all_users
    )



@app.route('/settings/users/<int:user_id>', methods=['POST'])
def update_settings(user_id):
    db = get_db()

    if VULNERABLE:
        # В уязвимом режиме игнорируем роли и любые проверки:
        # 1) Обновляем username для этого user_id
        new_username = request.form.get('username', '').strip()
        if new_username:
            db.execute(
                'UPDATE users SET username = ? WHERE id = ?;',
                (new_username, user_id)
            )

        # 2) Если в форме есть любые чекбоксы is_admin_<id>, обновляем роли для всех
        all_form_keys = request.form.keys()
        if any(key.startswith('is_admin_') for key in all_form_keys):
            all_users = db.execute('SELECT id FROM users;').fetchall()
            for row in all_users:
                print(row)
                uid = row['id']
                if request.form.get(f'is_admin_{uid}') == 'on':
                    new_role = 'admin'
                else:
                    new_role = 'user'

                print(new_role)
                db.execute(
                    'UPDATE users SET role = ? WHERE id = ?;',
                    (new_role, uid)
                )


        db.commit()
        print('commited')
        db.close()
        print('closed')
        return redirect(url_for('settings', user_id=user_id))

    # --- Защищённая версия ---
    if 'user_id' not in session:
        db.close()
        return redirect(url_for('login'))

    current_id   = session['user_id']
    current_role = session.get('role', '')

    if current_id != user_id and current_role != 'admin':
        db.close()
        return "Access Denied", 403

    # Читаем вновь роль из БД
    user = db.execute(
        'SELECT id, username, role FROM users WHERE id = ?;',
        (user_id,)
    ).fetchone()
    if not user:
        db.close()
        return "User not found", 404

    if current_role == 'admin':
        # Если админ, обновляем роли для всех
        all_users = db.execute('SELECT id FROM users;').fetchall()
        for row in all_users:
            uid = row['id']
            if request.form.get(f'is_admin_{uid}') == 'on':
                new_role = 'admin'
            else:
                new_role = 'user'
            db.execute(
                'UPDATE users SET role = ? WHERE id = ?;',
                (new_role, uid)
            )
        db.commit()
        db.close()
        return redirect(url_for('settings', user_id=user_id))

    # Иначе (обычный), обновляем только username
    new_username = request.form.get('username', '').strip()
    db.execute(
        'UPDATE users SET username = ? WHERE id = ?;',
        (new_username, user_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('settings', user_id=user_id))

