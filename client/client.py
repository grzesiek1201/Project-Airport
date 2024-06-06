import socket


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 65432))

    def send_response(self, message):
        try:
            self.s.sendall(message.encode("utf-8"))
            data = self.s.recv(1024)
        except socket.error as e:
            print("Socket error:", e)


if __name__ == "__main__":
    client = Client()
