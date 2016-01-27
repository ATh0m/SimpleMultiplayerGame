import threading
from . import Room


class WaitingRoom(threading.Thread):
    def __init__(self, new_clients):
        super().__init__()

        self.running = True
        self.last_id = 0

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
                    target_room = Room.Room(self.last_id)
                    self.last_id += 1
                    self.rooms.append(target_room)
                    target_room.start()

                target_room.users.append(user)
                target_room.free_slots -= 1
