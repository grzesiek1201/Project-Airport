import socket


class Server:
    def __init__(self, host, port, version):
        self.host = host
        self.port = port
        self.version = version

    class CommandError(Exception):
        pass

    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"Server listening on {self.host}: {self.port}")
                while True:
                    try:
                        conn, addr = s.accept()
                        with conn:
                            print(f"Connected to {addr}")
                            while True:
                                data = conn.recv(1024).decode("utf-8")
                                if not data:
                                    break
                                response = self.handle_command(data, conn, addr)
                                if response is None:
                                    print("Disconnected")
                                    break
                                conn.sendall(response.encode("utf-8"))
                    except KeyboardInterrupt:
                        print("KeyboardInterrupt: Stopping server...")
                        break
                    except Exception as e:
                        print(f"Error accepting connection: {e}")
        except OSError as e:
            print(f"Error binding to address {self.host}: {self.port}: {e}")

    def handle_command(self, command, conn, addr):
        try:
            command_parts = command.split()
            if not command_parts:
                raise self.CommandError("Empty command")

            command_name = command_parts[0].lower()
            command_args = command_parts[1:]

            command_handlers = {
            }

            handler = command_handlers.get(command_name)
            if not handler:
                raise self.CommandError("Unknown command")

            self.response = handler(*command_args)
            return self.response
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 65432
    server_version = "version: 0.1"
    server = Server(server_host, server_port, server_version)
    server.start()
