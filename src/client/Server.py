import threading
import socket
import pickle
from time import sleep
from . import Game


class Server:
    def __init__(self, player, enemy, ball):
        self.host = 'localhost'
        self.port = 1234

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.host, self.port))

        self.player = player
        self.enemy = enemy
        self.ball = ball

        self.sending_data = SendData(self.server, self.player)
        self.sending_data.start()

        self.receiving_data = ReceiveData(self.server, self.player, self.enemy, self.ball)
        self.receiving_data.start()

    def close(self):
        self.server.close()

        self.sending_data.running = False
        self.sending_data.join()

        self.receiving_data.running = False
        self.receiving_data.join()


class SendData(threading.Thread):
    def __init__(self, server, player):
        super().__init__()

        self.running = True
        self.server = server

        self.player = player

    def run(self):

        while self.running:
            try:
                data = {'STATUS': 'POSITION', 'DATA': {'PLAYER': {'x': self.player.x, 'y': self.player.y}}}

                data = pickle.dumps(data)

                self.server.send(data)

            except socket.error:
                self.running = False


class ReceiveData(threading.Thread):
    def __init__(self, server, player, enemy, ball):
        super().__init__()

        self.running = True
        self.server = server
        self.size = 1024

        self.data = None

        self.player = player
        self.enemy = enemy
        self.ball = ball

    def run(self):

        while self.running:
            try:
                data = self.server.recv(self.size)

                try:
                    self.data = pickle.loads(data)

                    if 'STATUS' in self.data:
                        if self.data['STATUS'] == 'POSITION':
                            if 'DATA' in self.data:
                                if "ENEMY" in self.data['DATA']:
                                    self.enemy.x, self.enemy.y = self.data['DATA']["ENEMY"]['x'], self.data['DATA']["ENEMY"]['y']
                                if "BALL" in self.data['DATA']:
                                    self.ball.x, self.ball.y = self.data['DATA']["BALL"]['x'], self.data['DATA']["BALL"]['y']

                        if self.data['STATUS'] == 'START':
                            if 'DATA' in self.data:
                                if self.data['DATA']['USER_NR'] == 0:
                                    self.player.x = 16
                                if self.data['DATA']['USER_NR'] == 1:
                                    self.player.x = 640 - 16

                except:
                    pass

            except socket.error:
                self.running = False
