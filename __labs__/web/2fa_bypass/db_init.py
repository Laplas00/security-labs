# db_init.py
import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

# ─── USERS ────────────────────────────────────────────────────────────────────
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE,
    twofa_code TEXT,
    twofa_pending_code TEXT
)
''')

# ─── POSTS (existing) ─────────────────────────────────────────────────────────
c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    author TEXT
)
''')

# ─── SEED USERS ─────────────────────────────────────────────────────────────────
# For now, each user gets a static 2FA code “123456”.
users = [
    ('admin', 'adminPass123', 'admin@example.com', '123456'),
    ('alice', 'AlicePass222', 'alice@example.com', '123456'),
    ('bob',   'bobpassA123',    'bob@example.com',   '123456'),
    ('carol', 'carolpassPP00PP','carol@example.com', '123456'),
]
for username, password, email, code in users:
    c.execute("""
        INSERT OR IGNORE INTO users (username, password, email, twofa_code)
        VALUES (?, ?, ?, ?)
    """, (username, password, email, code))

# ─── SEED POSTS ─────────────────────────────────────────────────────────────────
posts = [
    ('The Pain of Waking Up from Porn Addiction', 
     'How a glimpse into the past gave me hope for the future', 'admin'),
    ('The Importance of Wasting Time', 
     'In a culture that preaches capitalizing on every single moment, wasting time can provide peace and relief', 'admin'),
    ('Why We’re Afraid to Speak and What You Can Do to Break Free', 
     'The silent roots of language anxiety and how healing them unlocks fluency and freedom', 'admin'),
    ('How to Learn Anything Faster', 
     'Effective methods for acquiring new skills rapidly and retaining them long-term', 'admin'),
    ('Building Resilience in Difficult Times', 
     'Practical tips to strengthen your mental and emotional resilience during challenges', 'admin'),
]

for title, content, author in posts:
    c.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))

conn.commit()
conn.close()

