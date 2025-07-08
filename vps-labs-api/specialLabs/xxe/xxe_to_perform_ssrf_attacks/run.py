from multiprocessing import Process, Manager
import os
import socket
from app.routes.auth_funcs import *
from app.routes.posts import *
from app.routes.search import *
from app.routes.settings import *
from app.utils.vulns import get_vuln_flag
from flask import current_app

def run_main_app(shared_flag):
    ic('runned main app')
    app.config['shared_flag'] = shared_flag
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

def internal_listener(shared):
    ic('start iternal listener')
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 9000))
    s.listen()
    while True:
        print('iternal listener runned')
        conn, _ = s.accept()
        data = conn.recv(4096)
        # ловим точный GET /write_log?...
        if b"GET /write_log" in data:
            print('user passed1!!@##$!@#$!@#$!@#')
            shared['passed'] = True
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length:0\r\n\r\n")
        conn.close()

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flag = get_vuln_flag()
    print('FLAG:', flag, flush=True)

    with Manager() as manager:
        shared_flag = manager.dict()
        shared_flag["passed"] = False

        p1 = Process(target=run_main_app, args=(shared_flag,))
        print('process1 created')
        p2 = Process(target=internal_listener, args=(shared_flag,))        
        print('process2 created')
        p1.start()
        print('pr1 started')
        p2.start()
        print('pr2 started')
        p1.join()
        p2.terminate()
