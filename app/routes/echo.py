import gzip

def echo_handler(path, headers):
    echo_bytes = path.split("/echo/")[-1].encode()
    encodings = headers.get("Accept-Encoding", "").split(", ")

    content_type = "Content-Type: text/plain"
    status_line = "HTTP/1.1 200 OK"

    if "gzip" in encodings:
        encoding_header = "Content-Encoding: gzip\r\n"
        echo_bytes = gzip.compress(echo_bytes)

        content_len = f"Content-Length: {len(echo_bytes)}"
    else:
        encoding_header = ""
        content_len = f"Content-Length: {len(echo_bytes)}"

    http_res = f"{status_line}\r\n{encoding_header}{content_type}\r\n{content_len}\r\n\r\n".encode() + echo_bytes
    return http_res
