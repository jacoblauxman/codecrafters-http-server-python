import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        stream, _addr = server_socket.accept() # wait for client
        route_handler(stream)


def route_handler(stream):

        req_data = stream.recv(4096).decode()
        if not req_data:
            return

        req_lines = req_data.split("\r\n")
        method, path, version = req_lines[0].split(" ")

        if path == "/":
            http_res = "HTTP/1.1 200 OK\r\n\r\n"
            stream.send(http_res.encode())
        elif path.startswith("/echo/"):
            echo_res = echo_handler(path)
            stream.send(echo_res.encode())
        else:
            http_not_found = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
            stream.send(http_not_found.encode())

        stream.close()


def echo_handler(path):
    echo_str = path.split("/echo/")[-1]

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(echo_str)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{echo_str}\r\n\r\n"

    return http_res


if __name__ == "__main__":
    main()
