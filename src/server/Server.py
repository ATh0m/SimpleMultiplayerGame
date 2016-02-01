import logging
import queue
import socket
import sys
import threading
from . import Client
from . import Room
import shelve

logging.basicConfig(filename='logs.log',
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)-15s %(message)s')


class Server(threading.Thread):
    def __init__(self):
        super().__init__()

        self.host = ''
        self.port = 1234
        self.backlog = 5
        self.size = 1024

        self.server = None
        self.waiting_room = None

        self.running = False

        self.last_client_id = 0
        self.clients = []
        self.new_clients = queue.Queue()

        with shelve.open('database', 'c') as db:
            if 'PLAYERS' not in db.keys():
                db['PLAYERS'] = {}
            self.database = db['PLAYERS']

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

        self.waiting_room = Room.RoomController(self.new_clients)
        self.waiting_room.start()

        while self.running:

            try:
                connection = self.server.accept()

                client = Client.Client(connection, self.last_client_id)
                self.last_client_id += 1
                client.start()

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
            client.running = False
            client.join()

        for room in self.waiting_room.rooms:
            room.running = False
            room.join()

        self.server.close()

        self.waiting_room.running = False
        self.waiting_room.join()

        self.join()

        logging.info("Server stopped")


class ServerController:
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
            elif command.lower() == 'database':
                self.print_database()
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

    def print_clients(self):
        print(self.server.clients)

    def print_database(self):
        print(self.server.database)
