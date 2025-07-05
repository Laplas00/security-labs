from flask import Flask
import sqlite3
import os
import time

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))

app.secret_key = "FlaskUniqueSecretKey(it's a joke)"



def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn


