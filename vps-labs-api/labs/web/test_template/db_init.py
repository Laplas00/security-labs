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
users = [
    ('admin', 'adminPass123', 'admin'),
    ('alice', 'AlicePass222', 'user'),
    ('bob', 'bobpassA123', 'user'),
    ('carol', 'carolpassPP00PP', 'user'),
    ('dave', 'davepassIJIJI22', 'user'),
    ('eve', '0o0oOOevepass', 'user'),
]
for username, password, role in users:
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))

# Заполнение постов
posts = [
    ('The Pain of Waking Up from Porn Addiction', 
     'How a glimpse into the past gave me hope for the future', 'admin'),
    ('The Importance of Wasting Time', 
     'In a culture that preaches capitalizing on every single moment, wasting time can provide peace and relief', 'alice'),
    ('Why We’re Afraid to Speak and What You Can Do to Break Free', 
     'The silent roots of language anxiety and how healing them unlocks fluency and freedom', 'bob'),
    ('How to Learn Anything Faster', 
     'Effective methods for acquiring new skills rapidly and retaining them long-term', 'carol'),
    ('Building Resilience in Difficult Times', 
     'Practical tips to strengthen your mental and emotional resilience during challenges', 'dave'),
]

for title, content, author in posts:
    c.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))

conn.commit()
conn.close()

