import argparse
import os
import socket
from threading import Thread

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="File serving directory")
    args = parser.parse_args()

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        stream, _addr = server_socket.accept() # wait for client
        thread = Thread(target=route_handler, args=(stream, _addr, args.directory))
        thread.start()


def route_handler(stream, _addr, directory):

    while True:
        req_data = stream.recv(4096).decode()
        if not req_data:
            return

        req_lines = req_data.split("\r\n")
        print(f"REQ LINES:\n{req_lines}")
        method, path, version = req_lines[0].split(" ")
        user_agent = req_lines[2]
        body_content = req_lines[-1]

        if path == "/":
            http_res = "HTTP/1.1 200 OK\r\n\r\n"
            stream.send(http_res.encode())
        elif path.startswith("/echo/"):
            echo_res = echo_handler(path)
            stream.send(echo_res.encode())
        elif path.startswith("/user-agent"):
            ua_res = user_agent_handler(user_agent)
            stream.send(ua_res.encode())
        elif path.startswith("/files"):
            if method == "GET":
                get_file_res = get_file_handler(path, directory)
                stream.send(get_file_res.encode())
            elif method == "POST":
                pass
                post_file_res = post_file_handler(path, directory, body_content)
                stream.send(post_file_res.encode())
        else:
            http_not_found = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
            stream.send(http_not_found.encode())

        stream.close()


def echo_handler(path):
    echo_str = path.split("/echo/")[-1]

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(echo_str)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{echo_str}"

    return http_res

def user_agent_handler(user_agent):
    _ua_header, ua = user_agent.split(": ")

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(ua)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{ua}"

    return http_res

def get_file_handler(path, directory):
    filename = path.split("/files/")[-1]

    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            file_content = file.read()

            content_type = "Content-Type: application/octet-stream"
            content_len = f"Content-Length: {len(file_content)}"
            status_line = "HTTP/1.1 200 OK"
            http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{file_content}"

            return http_res
    else:
        http_not_found = "HTTP/1.1 404 NOT FOUND\r\n\r\n"

        return http_not_found

def post_file_handler(path, directory, content):
    filename = path.split("/files/")[-1]
    file_path = os.path.join(directory, filename)

    with open(file_path, "w") as file:
        file.write(content)

    return "HTTP/1.1 201 CREATED\r\n\r\n"


if __name__ == "__main__":
    main()
