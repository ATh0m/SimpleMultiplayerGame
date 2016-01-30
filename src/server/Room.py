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
                for user_target in self.users:
                    if user_target is not user:
                        # if user.data is not None:
                        try:
                            user_target.client.send(user.data)
                        except:
                            self.running = False
            sleep(3)
