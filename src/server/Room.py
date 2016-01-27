import threading
from time import sleep


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
            for user in self.users:
                user.client.send(bytes("{}".format(self.id), 'utf-8'))
            sleep(3)

            # for user in self.users:
            #     print()
            #     send data to all users in room