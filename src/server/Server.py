import logging
import queue
import socket
import sys
import threading
from . import Client
from . import WaitingRoom

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
        self.waiting_room = None

        self.running = False

        self.clients = []
        self.new_clients = queue.Queue()

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

        self.waiting_room = WaitingRoom.WaitingRoom(self.new_clients)
        self.waiting_room.start()

        while self.running:

            try:
                connection = self.server.accept()
                client = Client.Client(connection)

                self.clients.append(client)
                self.new_clients.put(client)

                _, address = connection

                logging.info('Connected ' + str(address[0]) + ':' + str(address[1]))
            except socket.error as error:
                logging.warning("Connection ERROR " + str(error))

    def stop(self):
        self.running = False

        for client in self.clients:
            client.client.close()

        for room in self.waiting_room.rooms:
            room.running = False
            room.join()

        self.server.close()

        self.waiting_room.running = False
        self.waiting_room.join()

        logging.info("Server stopped")