import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

# Таблица пользователей
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

# Таблица постов
c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    author TEXT
)
''')

# Заполнение пользователей
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('user', 'password', 'user')")

# Заполнение постов
c.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES ('Hello World', 'Welcome to our blog!', 'admin')")
c.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES ('Flask is Awesome', 'Flask makes web dev fun.', 'user')")

conn.commit()
conn.close()

