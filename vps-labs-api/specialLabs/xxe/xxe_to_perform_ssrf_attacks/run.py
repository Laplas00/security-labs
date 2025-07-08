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
    app.config['passed'] = shared_flag
    app.run(host='0.0.0.0', port=8000)

def internal_listener(shared_flag):
    ic('iternal litener launched')
    # A tiny internal HTTP server on port 9000
    HOST = "0.0.0.0"
    PORT = 9000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ic('socker runned')
        s.bind((HOST, PORT))
        s.listen()
        ic(f"Raw socket listening on {PORT} ...")
        while True:
            conn, addr = s.accept()
            with conn:
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
