import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432  # 1023 >

response_404 = """HTTP/1.1 404 NOT FOUND
 Date: {date}
 Server: Apache/2.2.14 (Win32)
 Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
 Content-Length: {length}
 Content-Type: text/html
 Connection: Closed

 <html><h1>Not Found</h1></html>
 """

response_ok = """HTTP/1.1 200 OK
Date: {date}
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: {length}
Content-Type: text/html
Connection: Closed

{body}"""

def hello(name):
    return f"Hello {name}!"

def get_request(conn: socket.socket) -> str:
    data = b""
    while True:
        data += conn.recv(1024)
        if data.endswith(b"\r\n\r\n"):
            break
    return data.decode("utf-8")

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((HOST, PORT))
socket_server.listen(1)

try:
    while True:
        conn, addr = socket_server.accept()
        with conn:
            request_data = get_request(conn)
            type_request, urn, _ = request_data.split("\r\n")[0].split(" ")
            print(type_request, urn)

            if urn.startswith("/hello/"):
                name = urn.split("/")[2]
                response_body = hello(name)
                response = response_ok.format(
                    date=datetime.now(),
                    length=len(response_body.encode()),
                    body=response_body,
                )
            else:
                try:
                    with open(urn.lstrip("//")) as file:
                        response_body = file.read()

                    response = response_ok.format(
                        date=datetime.now(),
                        length=len(response_body.encode()),
                        body=response_body,
                    )
                except:
                    response = response_404
            conn.sendall(response.encode())

except KeyboardInterrupt:
    socket_server.close()
