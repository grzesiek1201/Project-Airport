import socket


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send(self, message):
        self.client_socket.sendall(message.encode())
        response = self.client_socket.recv(1024)
        print(f'Received from server: {response.decode()}')

    def disconnect(self):
        self.client_socket.close()
