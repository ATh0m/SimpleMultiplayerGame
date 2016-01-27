import socket
import sys
import threading
import queue
import logging

logging.basicConfig(filename='logs.log',
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)-15s %(message)s')


class Server(threading.Thread):
    def __init__(self):
        super().__init__()

        self.host = ''
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None

        self.running = False

        self.clients = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
        except socket.error as error:
            value, message = error
            if self.server:
                self.server.close()
            logging.warning("Could not open socket: " + message)
            sys.exit(1)

    def run(self):
        self.open_socket()
        self.running = True

        logging.info("Server started")

        while self.running:

            try:
                connection, address = self.server.accept()
                self.clients.append((connection, address))
                logging.info('Connected ' + str(address[0]) + ':' + str(address[1]))
            except socket.error as error:
                logging.warning("Connection ERROR " + str(error))

    def stop(self):
        self.running = False

        for client in self.clients:
            connection, _ = client
            connection.close()

        self.server.close()

        logging.info("Server stopped")


class Client:
    def __init__(self):
        pass


class WaitingRoom(threading.Thread):
    def __init__(self):
        super().__init__()



class Room:
    def __init__(self):
        pass


class Controller:
    def __init__(self):
        self.server = None

    def run(self):
        running = 1

        while running:
            command = input('$: ')

            if command.lower() == 'start':
                self.start_server()
            elif command.lower() == 'stop':
                self.stop_server()
            elif command.lower() == 'close':
                self.close()
            else:
                print("Not known command")

    def start_server(self):
        if self.server is None:
            self.server = Server()
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

if __name__ == '__main__':
    c = Controller()
    c.run()
