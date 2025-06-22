import os

from app.routes.additional_renders import *
from app.routes.auth_funcs import *
from app.routes.posts import *
from app.routes.search import *
from app.routes.settings import *
from app.utils.vulns import get_vuln_flag
import threading

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flag = get_vuln_flag()
    print('FLAG:', flag)

    if flag == 'blind_ssrf_shellshock':
        from app.utils.iternal_api_for_blind_ssrf import run_internal_api
        # run api server in another thread
        t = threading.Thread(target=run_internal_api, daemon=True)
        t.start()
    app.run(host='0.0.0.0', port=8000, debug=False) 
