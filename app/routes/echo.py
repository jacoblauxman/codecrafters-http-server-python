def echo_handler(path, headers):
    echo_str = path.split("/echo/")[-1]
    encodings = headers.get("Accept-Encoding", "").split(", ")

    if any("gzip" in encoding for encoding in encodings):
        gzip = "Content-Encoding: gzip\r\n\r\n"
    else:
        gzip = ""

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(echo_str)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{gzip}{content_type}\r\n{content_len}\r\n\r\n{echo_str}"

    return http_res
