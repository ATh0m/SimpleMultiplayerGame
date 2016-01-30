import threading
import socket


class Client(threading.Thread):
    def __init__(self, connection, id):
        super().__init__()

        client, address = connection

        self.id = id
        self.client = client
        self.address = address
        self.size = 1024
        self.data = None

        self.running = True

    def run(self):

        while self.running:
            try:
                self.data = self.client.recv(self.size)
            except socket.error as error:
                self.running = False
