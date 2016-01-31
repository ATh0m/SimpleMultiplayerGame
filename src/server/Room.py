import threading
import pickle
import socket
from . import Game
import time


class Room(threading.Thread):
    def __init__(self, id):
        super().__init__()

        self.id = id
        self.users = []

        self.slots = 2
        self.free_slots = 2

        self.ball = Game.Ball()

        self.running = True

    def run(self):

        while self.running:

            if len(self.users) == 2:
                time.sleep(0.1)

                self.ball.movement(self.users[0], self.users[1])

                data0 = {'STATUS': 'POSITION',
                         'DATA': {"ENEMY": {"x": self.users[0].x, 'y': self.users[0].y},
                                  "BALL": {'x': self.ball.x, 'y': self.ball.y}}}
                data0 = pickle.dumps(data0)

                data1 = {'STATUS': 'POSITION',
                         'DATA': {"ENEMY": {"x": self.users[1].x, 'y': self.users[1].y},
                                  "BALL": {'x': self.ball.x, 'y': self.ball.y}}}
                data1 = pickle.dumps(data1)

                try:
                    self.users[0].client.send(data1)
                    self.users[1].client.send(data0)
                except socket.error as error:
                    # self.running = False
                    pass


class RoomController(threading.Thread):
    def __init__(self, new_clients):
        super().__init__()

        self.running = True
        self.last_room_id = 0

        self.new_clients = new_clients
        self.rooms = []

    def run(self):

        while self.running:

            if not self.new_clients.empty():

                user = self.new_clients.get()

                target_room = None

                for room in self.rooms:
                    if room.free_slots > 0:
                        target_room = room

                if target_room is None:
                    target_room = Room(self.last_room_id)
                    self.last_room_id += 1
                    self.rooms.append(target_room)
                    target_room.start()

                data = {"STATUS": "START", 'DATA': {'USER_NR': len(target_room.users), 'ROOM_NR': target_room.id}}
                data = pickle.dumps(data)

                user.client.send(data)

                target_room.users.append(user)
                target_room.free_slots -= 1
