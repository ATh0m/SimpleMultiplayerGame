import sys
from . import Server


class Controller:
    def __init__(self):
        self.server = None

    def run(self):
        running = True

        while running:
            command = input('$: ')

            if command.lower() == 'start':
                self.start_server()
            elif command.lower() == 'stop':
                self.stop_server()
            elif command.lower() == 'exit':
                self.close()
            elif command.lower() == 'clients':
                self.print_clients()
            else:
                print("Not known command")

    def start_server(self):
        if self.server is None:
            self.server = Server.Server()
            self.server.start()
            print("Server started")

    def stop_server(self):
        if self.server is not None:
            self.server.stop()
            self.server.join()

            self.server = None
            print("Server stopped")

    def close(self):
        self.stop_server()
        sys.exit(0)

    def print_clients(self):
        print(self.server.clients)