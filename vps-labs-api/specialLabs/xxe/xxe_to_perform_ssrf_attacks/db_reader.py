import sqlite3
conn = sqlite3.connect('blog.db')
c = conn.cursor()
for row in c.execute("SELECT username, verif_code FROM users"):
    print(row)
conn.close()

