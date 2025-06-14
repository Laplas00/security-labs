from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3


app = Flask(__name__)
app.secret_key = 'SomeSecret22'
VULNERABLE = os.getenv('VULNERABLE', '0') == '1'
pritn(VULNERABLE)


def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn



