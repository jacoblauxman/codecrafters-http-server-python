import socket

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    stream, _addr = server_socket.accept() # wait for client

    handler(stream)


def handler(stream):
    while True:

        req_data = stream.recv(4096).decode()
        if not req_data:
            break

        req_lines = req_data.split("\r\n")
        method, path, version = req_lines[0].split(" ")

        if path == "/":
            http_res = "HTTP/1.1 200 OK\r\n\r\n"

            stream.send(http_res.encode())
        else:
            http_not_found = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
            stream.send(http_not_found.encode())

        stream.close()


if __name__ == "__main__":
    main()
