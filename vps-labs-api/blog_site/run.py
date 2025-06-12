import os

from app.routes.auth_funcs import *
from app.routes.posts import *
from app.routes.search import *
from app.routes.settings import *
from app.utils.vulns import get_vuln_flags


if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flags = get_vuln_flags()
    print('FLAGS:', flags)
    app.run(host='0.0.0.0', port=5000, debug=True) # for traefic use 5000

