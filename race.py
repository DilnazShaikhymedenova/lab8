import pygame
import sys
import random
import time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60 #(how many frame in seconds)
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# Create a white screen
DISPLAYS = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy_pos):
        super().__init__()
        self.image = pygame.image.load("coin.jpeg")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        while self.rect.collidelist(enemy_pos) != -1:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global COINS_COLLECTED
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        elif pygame.sprite.spritecollideany(self, players):
            COINS_COLLECTED += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)


# Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin([E1.rect])

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
players = pygame.sprite.Group()
players.add(P1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1

pygame.time.set_timer(INC_SPEED, 1000)

while True:

    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYS.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYS.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYS.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)

        DISPLAYS.fill(RED)
        DISPLAYS.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    coins_collected_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    coins_collected_rect = coins_collected_text.get_rect()
    coins_collected_rect.topright = (SCREEN_WIDTH - 10, 10)
    DISPLAYS.blit(coins_collected_text, coins_collected_rect)

    pygame.display.update()
    FramePerSec.tick(FPS)