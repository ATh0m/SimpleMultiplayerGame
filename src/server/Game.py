class Ball:
    def __init__(self):
        self.x, self.y = 320, 240
        self.speed_x = -10
        self.speed_y = 10
        self.size = 8

    def movement(self, player1, player2):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y <= 0:
            self.speed_y *= -1
        elif self.y >= 480 - self.size:
            self.speed_y *= -1

        if self.x <= 0:
            self.__init__()
        elif self.x >= 640 - self.size:
            self.__init__()
            # self.speed_x = 3

        for n in range(-self.size, 64):
            if self.y == player1.y + n:
                if self.x <= player1.x + 8:
                    self.speed_x *= -1
                    break
            n += 1

        for n in range(-self.size, 64):
            if self.y == player2.y + n:
                if self.x >= player2.x - 8:
                    self.speed_x *= -1
                    break
            n += 1
