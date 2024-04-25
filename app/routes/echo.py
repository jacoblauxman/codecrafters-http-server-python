def echo_handler(path):
    echo_str = path.split("/echo/")[-1]

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(echo_str)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{echo_str}"

    return http_res
