import socket
import threading


class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f'Server listening on {self.host}:{self.port}')

    def start(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f'Connection from {client_address}')
                handler_thread = threading.Thread(target=self.handle, args=(client_socket,))
                handler_thread.start()
        except Exception as e:
            print(f'Server error: {e}')
        finally:
            self.stop()

    def handle(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f'Received data: {data.decode()}')
                client_socket.sendall(data)
        except Exception as e:
            print(f'Handler error: {e}')
        finally:
            client_socket.close()

    def stop(self):
        self.server_socket.close()
