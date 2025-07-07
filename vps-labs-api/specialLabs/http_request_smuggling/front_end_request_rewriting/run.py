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

def proxy_listener(shared_flag):
    FRONT_PORT = 9000                  # сюда шлёт студент
    BACK_HOST, BACK_PORT = "127.0.0.1", 8000  # где крутится Flask

    def handle(client, addr):
        with client, socket.create_connection((BACK_HOST, BACK_PORT)) as backend:
            raw = client.recv(65535)   # берём всё, нам хватит

            # --- front-end header rewriting только ПЕРВОГО запроса ---
            head_end = raw.find(b"\r\n\r\n")
            first, rest = raw[:head_end+4], raw[head_end+4:]

            # убираем возможный X-Orig-IP и вставляем свой
            first = re.sub(rb"(?i)^X-Orig-IP:.*?\r\n", b"", first, flags=re.MULTILINE)
            req_line, remain = first.split(b"\r\n", 1)
            first = b"\r\n".join([
                req_line,
                f"X-Orig-IP: {addr[0]}\r\n".encode() + remain
            ])

            backend.sendall(first + rest)      # прокидываем дальше

            # ответ — просто труба
            while (chunk := backend.recv(4096)):
                client.sendall(chunk)

            # для простого «индикатора успеха» в админке
            if b"0\r\n\r\n" in raw and b"GET /debug" in raw:
                shared_flag["flag_taken"] = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", FRONT_PORT))
        s.listen()
        print(f"[proxy] listening on :{FRONT_PORT}")
        while True:
            c, a = s.accept()
            threading.Thread(target=handle, args=(c, a), daemon=True).start()

if __name__ == '__main__':
    if not os.path.exists('blog.db'):
        import db_init  # инициализация базы при первом запуске

    flag = get_vuln_flag()
    print('FLAG:', flag, flush=True)

    with Manager() as manager:
        shared_flag = manager.dict()
        shared_flag["flag_taken"] = False

        p1 = Process(target=run_main_app, args=(shared_flag,))
        p2 = Process(target=proxy_listener, args=(shared_flag,))        

        p1.start()
        p2.start()
        p1.join()
        p2.terminate()
