import os

def get_file_handler(path, directory):
    filename = path.split("/files/")[-1]

    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            file_content = file.read()

            content_type = "Content-Type: application/octet-stream"
            content_len = f"Content-Length: {len(file_content)}"
            status_line = "HTTP/1.1 200 OK"
            http_res = f"{status_line}\r\n{content_type}\r\n{content_len}\r\n\r\n{file_content}".encode()

            return http_res
    else:
        http_not_found = "HTTP/1.1 404 Not Found\r\n\r\n"

        return http_not_found

def post_file_handler(path, directory, content):
    filename = path.split("/files/")[-1]
    file_path = os.path.join(directory, filename)

    with open(file_path, "w") as file:
        file.write(content)

    return "HTTP/1.1 201 Created\r\n\r\n".encode()
