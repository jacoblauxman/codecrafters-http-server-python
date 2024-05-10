from .echo import echo_handler
from .files import get_file_handler, post_file_handler
from .user_agent import user_agent_handler

def route_handler(stream, directory):

    while True:
        req_data = stream.recv(4096).decode()
        if not req_data:
            return

        req_lines = req_data.split("\r\n")

        method, path, version = req_lines[0].split(" ")
        headers = parse_headers(req_lines)
        body_content = req_lines[-1]

        if path == "/":
            http_res = "HTTP/1.1 200 OK\r\n\r\n".encode()
            stream.send(http_res)

        elif path.startswith("/echo/"):
            echo_res = echo_handler(path, headers)
            stream.send(echo_res)

        elif path.startswith("/user-agent"):
            ua_res = user_agent_handler(headers)
            stream.send(ua_res)

        elif path.startswith("/files"):
            if method == "GET":
                get_file_res = get_file_handler(path, directory)
                stream.send(get_file_res)

            elif method == "POST":
                post_file_res = post_file_handler(path, directory, body_content)
                stream.send(post_file_res)

        else:
            http_not_found = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            stream.send(http_not_found)

        stream.close()


def parse_headers(req_lines):
    headers = {}

    lines = req_lines[1:]
    for line in lines:
        if line == '':
            break
        key, val = line.split(": ", 1)
        headers[key] = val

    return headers
