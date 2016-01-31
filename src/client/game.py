import pygame
from . import Server


class Player:
    def __init__(self):
        self.x, self.y = 16, SCR_HEI / 2
        self.speed = 8
        self.padWid, self.padHei = 8, 64

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        elif keys[pygame.K_s]:
            self.y += self.speed

        if self.y <= 0:
            self.y = 0
        elif self.y >= SCR_HEI - 64:
            self.y = SCR_HEI - 64

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))


class Enemy:
    def __init__(self):
        self.x, self.y = SCR_WID - 16, SCR_HEI / 2
        self.speed = 8
        self.padWid, self.padHei = 8, 64

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))


class Ball:
    def __init__(self):
        self.x, self.y = SCR_WID / 2, SCR_HEI / 2
        self.speed_x = -5
        self.speed_y = 5
        self.size = 8

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 8, 8))


SCR_WID, SCR_HEI = 640, 480
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Pong")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

ball = Ball()
player = Player()
enemy = Enemy()

server = Server.Server(player, enemy, ball)

while True:
    # process
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game exited by user")

            server.close()

            exit()
            # process
            # logic
    player.movement()
    # logic
    # draw
    screen.fill((0, 0, 0))
    ball.draw()
    player.draw()
    enemy.draw()
    # draw
    # _______
    pygame.display.flip()
    clock.tick(FPS)