
import os
from app.routes.auth_funcs import *
from app.routes.posts import *
from app.routes.search import *
from app.routes.settings import *
from app.utils.vulns import get_vuln_flag

def run_main_app():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flag = get_vuln_flag()
    print('FLAG:', flag, flush=True)
    run_main_app()

