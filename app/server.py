import os
import socket
from threading import Thread

from app.routes.router import route_handler

def start_server(dir):
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)


    while True:
        stream, _addr = server_socket.accept()
        thread = Thread(target=route_handler, args=(stream, dir))
        thread.start()
