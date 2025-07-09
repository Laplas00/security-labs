from flask import Flask
import os, secrets, sqlite3
import secrets

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.secret_key = "FlaskUniqueSecretKey(it's a joke)"
app.config['SECRET_KEY'] = secrets.token_hex(32)

print('app init')


def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn


