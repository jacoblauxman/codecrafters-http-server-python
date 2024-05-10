def user_agent_handler(headers):
    ua = headers.get("User-Agent", "")

    content_type = "Content-Type: text/plain"
    content_len = f"Content-Length: {len(ua)}"
    status_line = "HTTP/1.1 200 OK"
    http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{ua}"

    return http_res
