import pygame
from . import Server


class Player:
    def __init__(self, screen, width, height, username):
        self.screen = screen
        self.width = width
        self.height = height

        self.x, self.y = 16, self.height / 2
        self.speed = 8
        self.padWid, self.padHei = 8, 64

        self.points = 0
        self.username = username
        self.username_font = pygame.font.Font("client/imagine_font.ttf", 30)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        elif keys[pygame.K_s]:
            self.y += self.speed

        if self.y <= 0:
            self.y = 0
        elif self.y >= self.height - 64:
            self.y = self.height - 64

    def draw(self):
        score_blit = self.username_font.render(str(self.username), 1, (0, 0, 0))
        self.screen.blit(score_blit, (32, 16))

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.padWid, self.padHei))


class Enemy:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.x, self.y = self.width - 16, self.height / 2
        self.padWid, self.padHei = 8, 64

        self.username = ''
        self.username_font = pygame.font.Font("client/imagine_font.ttf", 30)

    def draw(self):
        score_blit = self.username_font.render(str(self.username), 1, (255, 255, 255))
        self.screen.blit(score_blit, (self.height + 92, 16))

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.padWid, self.padHei))


class Ball:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.x, self.y = self.width / 2, self.height / 2
        self.size = 8

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.size, self.size))


class Game:
    def __init__(self, username, server_address):
        self.screen_width = 640
        self.screen_height = 480

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.ball = Ball(self.screen, self.screen_width, self.screen_height)
        self.player = Player(self.screen, self.screen_width, self.screen_height, username)
        self.enemy = Enemy(self.screen, self.screen_width, self.screen_height)

        self.server = Server.Server(self.player, self.enemy, self.ball, server_address, username)

        self.running = True

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Game exited by user")
                    self.server.close()
                    exit()
            self.player.movement()
            self.screen.fill((255, 255, 255))
            self.ball.draw()
            self.player.draw()
            self.enemy.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
