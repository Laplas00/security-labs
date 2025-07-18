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
    app.config['shared_flag'] = shared_flag
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

def raw_socket_listener(shared_flag):
    HOST = "0.0.0.0"
    PORT = 9000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('socker runned')
        s.bind((HOST, PORT))
        s.listen()
        print(f"Raw socket listening on {PORT} ...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                ic(data)
                # "0\r\n\r\nGET /clte" in raw
                if b"0\r\n\r\nGET /tecl" in data:
                    print("TE.CL Smuggling detected!")
                    shared_flag["te_cl"] = True

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flag = get_vuln_flag()
    print('FLAG:', flag, flush=True)

    with Manager() as manager:
        shared_flag = manager.dict()
        shared_flag["te_cl"] = False

        p1 = Process(target=run_main_app, args=(shared_flag,))
        p2 = Process(target=raw_socket_listener, args=(shared_flag,))        

        p1.start()
        p2.start()
        p1.join()
        p2.terminate()
