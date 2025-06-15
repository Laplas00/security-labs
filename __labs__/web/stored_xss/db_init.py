import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

# Users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

# Posts
c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    author TEXT
)
''')

# Comments (for stored XSS lab)
c.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    message TEXT
)
''')

# Seed users
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

# Seed posts
posts = [
    ('The Pain of Waking Up from Porn Addiction', 'How a glimpse into the past gave me hope for the future', 'admin'),
    ('The Importance of Wasting Time', 'In a culture that preaches capitalizing on every single moment, wasting time can provide peace and relief', 'admin'),
    ('Why We’re Afraid to Speak and What You Can Do to Break Free', 'The silent roots of language anxiety and how healing them unlocks fluency and freedom', 'admin'),
    ('How to Learn Anything Faster', 'Effective methods for acquiring new skills rapidly and retaining them long-term', 'admin'),
    ('Building Resilience in Difficult Times', 'Practical tips to strengthen your mental and emotional resilience during challenges', 'admin'),
]
for title, content, author in posts:
    c.execute("INSERT OR IGNORE INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))

# Seed comments
comments = [
    "This project changed how I see the web!",
    "I love the design. Very clean.",
    "I think there's a bug in the second example.",
    "Can we get a dark mode?",
    "This helped me understand XSS so well.",
    "I tried the lab and it really clicked.",
    "Minimalist UI for the win.",
    "My teacher recommended this site.",
    "Can't believe I missed this attack before.",
    "Looking forward to more labs like this!"
]
for msg in comments:
    c.execute("INSERT INTO comments (message) VALUES (?)", (msg,))

conn.commit()
conn.close()

