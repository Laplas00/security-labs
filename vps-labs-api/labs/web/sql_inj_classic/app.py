
from core import *

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске
    app.run(host='0.0.0.0', port=5000) # for traefic use 5000

