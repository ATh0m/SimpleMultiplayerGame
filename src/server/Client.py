import threading
import socket
import pickle
import simplejson


class Client(threading.Thread):
    def __init__(self, connection, id):
        super().__init__()

        client, address = connection

        self.id = id
        self.client = client
        self.address = address
        self.size = 1024
        self.data = None

        self.position = {'x': 0, 'y': 0}

        self.running = True

    def run(self):

        while self.running:
            try:
                data = self.client.recv(1024)
                # print(data.decode('utf-8'))
                # self.data = simplejson.loads(data.decode('utf-8'))

                try:
                    self.data = pickle.loads(data)

                    if 'STATUS' in self.data:
                        if self.data['STATUS'] == 'POSITION':
                            if 'DATA' in self.data:
                                if 'PLAYER' in self.data['DATA']:
                                    self.position['x'] = self.data['DATA']['PLAYER']['x']
                                    self.position['y'] = self.data['DATA']['PLAYER']['y']
                except:
                    pass

            except socket.error as error:
                self.running = False
