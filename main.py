"""
LICENSES
The Pixel Emulator Font is by Pixel Sagas at https://www.fontspace.com/pixel-emulator-font-f21507
"""

import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
global collected
collected = 0

# image loading
global player_empty, player_quarter, player_half, player_most, player_full
player_empty = pygame.image.load("cookie_catch/assets/player_empty.png")
player_quarter = pygame.image.load("cookie_catch/assets/player_quarter.png")
player_half = pygame.image.load("cookie_catch/assets/player_half.png")
player_most = pygame.image.load("cookie_catch/assets/player_most.png")
player_full = pygame.image.load("cookie_catch/assets/player_full.png")
icon = pygame.image.load("cookie_catch/assets/icon.png")


# cookie jar class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = player_empty
        self.surf.set_colorkey((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.x = 400
        self.rect.y = 460

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        if collected == 15:
            self.surf = player_quarter
            self.surf.set_colorkey((255, 0, 0))
        if collected == 40:
            self.surf = player_half
            self.surf.set_colorkey((255, 0, 0))
        if collected == 75:
            self.surf = player_most
            self.surf.set_colorkey((255, 0, 0))
        if collected == 100:
            self.surf = player_full
            self.surf.set_colorkey((255, 0, 0))


# falling cookies class
class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super(Cookie, self).__init__()
        self.surf = pygame.image.load("cookie_catch/assets/cookie.png")
        self.surf.set_colorkey((0, 0, 255))
        self.rect = self.surf.get_rect(
            center=(random.randint(3, SCREEN_WIDTH-3), 0)
        )

    def update(self):
        global collected

        self.rect.move_ip(0, 5)
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        if self.rect.colliderect(player.rect):
            collected += 1
            self.kill()


# initialize Pygame
pygame.init()

pygame.display.set_caption("Cookie Catch!")
pygame.display.set_icon(icon)

ADD_COOKIE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_COOKIE, 1000)

player = Player()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load("cookie_catch/assets/background.png")
font = pygame.font.Font("cookie_catch/assets/pixel_emulator.ttf", 50)

cookies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

# game loop
running = True
while running:
    screen.blit(background, (0, 0))
    text = font.render(str(collected), False, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADD_COOKIE:
            new_cookie = Cookie()
            cookies.add(new_cookie)
            all_sprites.add(new_cookie)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pressed = pygame.key.get_pressed()
    screen.blit(player.surf, player.rect)
    player.update(pressed)

    cookies.update()

    screen.blit(text, (35, 30))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
