import threading


class Client(threading.Thread):
    def __init__(self, connection):
        super().__init__()

        client, address = connection

        self.client = client
        self.address = address
        self.size = 1024
        self.data = ""