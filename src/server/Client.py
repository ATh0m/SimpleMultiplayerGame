import threading
import socket
import pickle


class Client(threading.Thread):
    def __init__(self, connection, id):
        super().__init__()

        client, address = connection

        self.id = id
        self.client = client
        self.address = address
        self.size = 1024
        self.data = None

        self.x = 0
        self.y = 0
        self.username = ''
        self.score = 0

        self.running = True

    def run(self):

        while self.running:
            try:
                data = self.client.recv(self.size)

                try:
                    self.data = pickle.loads(data)

                    if 'STATUS' in self.data:
                        if self.data['STATUS'] == 'POSITION':
                            if 'DATA' in self.data:
                                if 'PLAYER' in self.data['DATA']:
                                    self.x = self.data['DATA']['PLAYER']['x']
                                    self.y = self.data['DATA']['PLAYER']['y']
                                    self.username = self.data['DATA']['PLAYER']['USERNAME']
                except:
                    pass

            except socket.error as error:
                self.running = False
