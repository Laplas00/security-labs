
import os
from multiprocessing import Process

from app.routes.auth_funcs import *
from app.routes.posts import *
from app.routes.search import *
from app.routes.settings import *
from app.utils.vulns import get_vuln_flag

def run_main_app():
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flag = get_vuln_flag()
    print('FLAG:', flag, flush=True)

    processes = []
    if flag == 'open_redirect_to_ssrf_chain':
        # Запуск internal_api как отдельного процесса
        from app.utils.iternal_api_for_blind_ssrf import run_internal_api
        p = Process(target=run_internal_api)
        p.start()
        processes.append(p)

    run_main_app()

