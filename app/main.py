import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    stream, _addr = server_socket.accept() # wait for client

    handler(stream)


def handler(stream):
    stream.recv(4096)

    http_res = "HTTP/1.1 200 OK\r\n\r\n"

    stream.send(http_res.encode())


if __name__ == "__main__":
    main()
