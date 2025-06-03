import os
if not os.path.exists('blog.db'):
    import db_init  # инициализация базы при первом запуске


from core import *



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # for traefic use 5000

