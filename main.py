from server.server import Server
from client.client import Client
import threading


def run_server():
    server = Server()
    server.start()


def run_client():
    client = Client()
    client.connect()
    client.send("Hello, Server!")
    client.disconnect()


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    run_client()
