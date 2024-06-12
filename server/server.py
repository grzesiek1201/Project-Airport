import socket
from .handler import ClientHandler


class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def start(self):
        print(f'Server listening on {self.host}:{self.port}')
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f'Connection from {client_address}')
            handler = ClientHandler(client_socket)
            handler.handle()

    def stop(self):
        self.server_socket.close()
