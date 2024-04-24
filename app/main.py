import socket
from threading import Thread

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        stream, _addr = server_socket.accept() # wait for client
        # route_handler(stream)
        thread = Thread(target=route_handler, args=(stream,))
        thread.start()


def route_handler(stream):

    while True:
        req_data = stream.recv(4096).decode()
        if not req_data:
            return

        req_lines = req_data.split("\r\n")
        method, path, version = req_lines[0].split(" ")
        user_agent = req_lines[2]

        if path == "/":
            http_res = "HTTP/1.1 200 OK\r\n\r\n"
            stream.send(http_res.encode())
        elif path.startswith("/echo/"):
            echo_res = echo_handler(path)
            stream.send(echo_res.encode())
        elif path.startswith("/user-agent"):
            # ua_res = user_agent_handler(req_lines)
            ua_res = user_agent_handler(user_agent)
            stream.send(ua_res.encode())
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

def user_agent_handler(user_agent):
    print(f"HERE: {user_agent}")
    _ua_header, ua = user_agent.split(": ")

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(ua)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{ua}\r\n\r\n"

    return http_res



if __name__ == "__main__":
    main()
