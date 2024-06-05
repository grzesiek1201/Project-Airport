from server import Server


class Main:
    host = "127.0.0.1"
    port = 65432
    version = "version: 0.1"


if __name__ == "__main__":
    Server.start()
