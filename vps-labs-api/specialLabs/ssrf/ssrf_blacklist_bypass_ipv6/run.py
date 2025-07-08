
from multiprocessing import Process, Manager
import os, socket
from flask import current_app, request, send_file
from app.utils.vulns import get_vuln_flag
from app.utils.app import app, get_db
from app.routes.auth_funcs import *
from app.routes.posts import *
from app.routes.search import *
from app.routes.settings import *


def run_main_app(shared_flag):
    app.config['ssrf_passed'] = shared_flag

    print('app runned')
    app.run(host='0.0.0.0', port=8000)


def internal_listener(shared_flag):
    # A tiny internal HTTP server on port 9000
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
                ic(data.decode())
                # Check for the write_log endpoint
                if b"POST /write_log" in data:
                    for line in data.split(b"\r\n"):
                        conditions_to_accept = b'%5B' in line or b'%5D' in line

                        print('---')
                        if b'new+avatar+for+testuser&avatar_url' in line:
                            print(line)
                            print(line.decode())#
                            print(line.split(b':'))
                            # Host: [::1]:9000  (or another IPv6)
                            if conditions_to_accept:
                                shared_flag["ssrf_passed"] = True
                                print("✅ SSRF IPv6 bypass detected!")
                            else:
                                pass
                # Always send a simple HTTP 200 OK back
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length:0\r\n\r\n")
                conn.close()

if __name__ == "__main__":
    if not os.path.exists('blog.db'):
        import db_init

    flag = get_vuln_flag()
    print("FLAG:", flag)

    with Manager() as manager:
        shared_flag = manager.dict()
        shared_flag["ssrf_passed"] = False

        p1 = Process(target=run_main_app, args=(shared_flag,))
        p2 = Process(target=internal_listener, args=(shared_flag,))
        p1.start()
        p2.start()
        p1.join()
        p2.terminate()
