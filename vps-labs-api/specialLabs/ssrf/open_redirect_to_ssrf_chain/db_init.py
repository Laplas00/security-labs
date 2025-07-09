import sqlite3
import random

conn = sqlite3.connect('blog.db')
c = conn.cursor()

# Таблица пользователей
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT,
    verif_code TEXT,
    role TEXT
);
''')

# Таблица постов
c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    author TEXT
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER,
    author TEXT,
    content TEXT,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
''')

# Заполнение пользователей
users = [
    ('BlogCreator', 'adminPass123', 'admin', 'admin@email.com',f"{random.randint(1000, 9999):04d}"),
    ('alice', 'AlicePass222', 'user','alice@email.com', f"{random.randint(1000, 9999):04d}"),
    ('bob', 'bobpassA123', 'user', 'bobmilo@email.com',f"{random.randint(1000, 9999):04d}"),
    ('carol', 'carolpassPP00PP', 'user', 'carol@email.com', f"{random.randint(1000, 9999):04d}"),
    ('dave', 'davepassIJIJI22', 'user', 'dave@email.com', f"{random.randint(1000, 9999):04d}"),
    ('eve', '0o0oOOevepass', 'user', 'eve@email.com', f"{random.randint(1000, 9999):04d}"),
    ('testuser', 'testpass', 'user', 'test@email.com', "1234"),

]
for username, password, role, email, verif in users:
    c.execute("INSERT OR IGNORE INTO users (username, password, role, email, verif_code) VALUES (?, ?, ?, ?, ?)", (username, password, role, email, verif))

# Заполнение постов
posts = [
    ('The Pain of Waking Up from Porn Addiction', 
     'How a glimpse into the past gave me hope for the future', 'BlogCreator'),
    ('The Importance of Wasting Time', 
     'In a culture that preaches capitalizing on every single moment, wasting time can provide peace and relief', 'BlogCreator'),
    ('Why We’re Afraid to Speak and What You Can Do to Break Free', 
     'The silent roots of language anxiety and how healing them unlocks fluency and freedom', 'BlogCreator'),
    ('How to Learn Anything Faster', 
     'Effective methods for acquiring new skills rapidly and retaining them long-term', 'BlogCreator'),
    ('Building Resilience in Difficult Times', 
     'Practical tips to strengthen your mental and emotional resilience during challenges', 'BlogCreator'),
]

for title, content, author in posts:
    c.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))

# (По желанию) Заполнить комментарии:
sample_comments = [
    (1, 'alice', 'Great post!'),
    (1, 'bob', 'This hit home.'),
    (2, 'carol', 'Time management is overrated ;)'),
    (3, 'dave', 'Thanks for the advice!'),
    (4, 'eve', 'Very useful tips!'),
]
for post_id, author, content in sample_comments:
    c.execute("INSERT OR IGNORE INTO comments (post_id, author, content) VALUES (?, ?, ?)", (post_id, author, content))

conn.commit()
conn.close()

