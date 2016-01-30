import threading
import socket


class Connection:
    def __init__(self):
        self.host = 'localhost'
        self.port = 1234

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.host, self.port))


class SendData(threading.Thread):
    def __init__(self, server, data):
        super().__init__()

        self.running = True
        self.server = server

        self.data = data

    def run(self):

        while self.running:
            try:
                self.server.send(self.data)
            except socket.error:
                self.running = False


class ReceiveData(threading.Thread):
    def __init__(self, server):
        super().__init__()

        self.running = True
        self.server = server
        self.size = 1024

        self.data = None

    def run(self):

        while self.running:
            try:
                self.data = self.server.recv(self.size)
            except socket.error:
                self.running = False
