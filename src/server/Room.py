import threading


class Room(threading.Thread):
    def __init__(self):
        super().__init__()

        self.users = []

        self.slots = 2
        self.free_slots = 2

    def run(self):

        running = True

        if running:
            for user in self.users:
                pass
#                 send data to all users in room