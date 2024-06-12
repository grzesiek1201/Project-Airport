class ClientHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f'Received data: {data.decode()}')
                self.client_socket.sendall(data)
        finally:
            self.client_socket.close()
