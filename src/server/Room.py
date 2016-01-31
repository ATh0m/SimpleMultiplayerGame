import threading
import simplejson
import pickle
import socket
from time import sleep
from random import randint


class Room(threading.Thread):
    def __init__(self, id):
        super().__init__()

        self.id = id
        self.users = []

        self.slots = 2
        self.free_slots = 2

        self.running = True

    def run(self):

        while self.running:

            data = {'STATUS': 'POSITION', 'DATA': {"ENEMY": {"x": randint(100, 400), 'y': 50}, "BALL": {'x': randint(100, 400), 'y': 100}}}
            # data = simplejson.dumps(data)
            data = pickle.dumps(data)

            for user in self.users:
                try:
                    user.client.send(data)
                    # sleep(0.0001)
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

                data = {"STATUS": "OK"}
                # data = simplejson.dumps(data)

                data = pickle.dumps(data)

                user.client.send(data)

                target_room.users.append(user)
                target_room.free_slots -= 1
