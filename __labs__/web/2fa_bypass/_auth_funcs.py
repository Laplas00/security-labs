from _libs import *

@app.route('/logout')
def logout():
    session.clear()
    flash('Login success')
    return redirect(url_for('index'))


# helper functions
def query_user_by_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user


def query_user_by_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user



# ─── LOGIN (step 1) ────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()

        if user and user["password"] == password:
            # Generate a random 6-digit code and store it
            code = ''.join(random.choices(string.digits, k=6))
            db = get_db()
            db.execute("UPDATE users SET twofa_pending_code = ? WHERE id = ?", (code, user["id"]))
            db.commit()
            db.close()

            # (In a real lab, you’d email this code. For now you can print it.)
            print(f"=== 2FA code for {email} is: {code} ===")

            # Mark that the user has passed step 1
            session.clear()
            session["pre_2fa_user"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("enter_2fa"))

        flash("Invalid email or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/enter-2fa")
def enter_2fa():
    # If someone goes here without logging in first, redirect them to /login
    if "pre_2fa_user" not in session:
        return redirect(url_for("login"))
    return render_template("enter_2fa.html")

 


# ─── VERIFY 2FA (step 2 - POST) ─────────────────────────────────────────────────
@app.route("/verify-2fa", methods=["POST"])
def verify_2fa():
    """
    Expects JSON { "code": "xxxxxx" }.
    Vulnerable: always returns success:false.
    Secure: checks the code against the DB and if correct, sets session flag.
    """
    data = request.get_json() or {}
    entered_code = data.get("code", "").strip()
    user_id = session.get("pre_2fa_user")

    if not user_id:
        return jsonify({"success": False, "error": "no_pre_2fa"}), 400

    if VULNERABLE:
        # Vuln: tell client "2FA failed" every time, forcing interception
        return jsonify({"success": False})

    # Secure mode: actually verify code
    db = get_db()
    user = db.execute("SELECT twofa_pending_code FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()

    if user and user["twofa_pending_code"] == entered_code:
        # Mark this user as “2FA verified” in session
        session["twofa_verified"] = True
        return jsonify({"success": True})

    return jsonify({"success": False})

# ─── FINALIZE LOGIN (step 3) ─────────────────────────────────────────────────────
@app.route("/finalize-login", methods=["POST"])
def finalize_login():
    """
    In a real app, this would check server‐side that 2FA succeeded (e.g. session["twofa_verified"] == True).
    But in our vulnerable variant, we trust the front end’s call unconditionally if VULNERABLE == "1".
    """
    print("Finalize login")
    user_id = session.get("pre_2fa_user")

    if not user_id:
        return jsonify({"error": "no_pre_2fa"}), 400

    if VULNERABLE:
        # Vuln: Just set session["user_id"] even though we never verified 2FA
        session.pop("pre_2fa_user", None)
        session["user_id"] = user_id
        return jsonify({"success": True})

    # Secure flow: only finalize if 2FA was actually verified
    if session.get("twofa_verified"):
        session.pop("pre_2fa_user", None)
        session["user_id"] = user_id
        session.pop("twofa_verified", None)
        flush('Login success')
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "2fa_not_verified"}), 403


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        if VULNERABLE:
            # Уязвимый SQL: прямое включение данных пользователя
            try:
                query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
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
                    'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                    (username, password, email)
                )
                db.commit()
                flash('Registration complete, login!')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already in use')
    return render_template('register.html')


