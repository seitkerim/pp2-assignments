import pygame
import sys
import random
import os
from pygame.locals import *

pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont("Verdana", 30)

score = 0
coins_collected = 0
speed = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(IMAGES_DIR, "enemy.png"))
        self.image = pygame.transform.smoothscale(img, (90, 140))
        self.rect = self.image.get_rect()
        self.reset()

    # сбрасывает врага на случайную позицию сверху экрана
    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -150

    # двигает врага вниз, увеличивает счёт и скорость когда враг уходит за экран
    def move(self):
        global score, speed
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            speed += 0.2
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(IMAGES_DIR, "car.png"))
        self.image = pygame.transform.smoothscale(img, (90, 140))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)

    # обрабатывает нажатия клавиш и двигает машину влево/вправо не выходя за края
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(7, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(os.path.join(IMAGES_DIR, "coin.png"))
        self.base_image = pygame.transform.smoothscale(img, (40, 40))
        self.reset()

    # генерирует монету со случайной ценностью (1-3) и размером зависящим от ценности
    def reset(self):
        self.rect = self.base_image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300, -50)
        self.value = random.randint(1, 3)
        size = 30 + self.value * 10  # чем ценнее монета тем она больше
        self.image = pygame.transform.smoothscale(self.base_image, (size, size))
        self.rect = self.image.get_rect(center=self.rect.center)

    # двигает монету вниз, сбрасывает если ушла за экран
    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


P1 = Player()
E1 = Enemy()
C1 = Coin()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
    C1.move()

    # если игрок столкнулся с врагом — показываем Game Over и выходим
    if pygame.sprite.collide_rect(P1, E1):
        text = font.render("GAME OVER", True, BLACK)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        DISPLAYSURF.blit(text, rect)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # если игрок подобрал монету — добавляем её ценность к счётчику
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += C1.value
        C1.reset()

    DISPLAYSURF.fill(GRAY)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)

    DISPLAYSURF.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    DISPLAYSURF.blit(font.render(f"Coins: {coins_collected}", True, WHITE), (SCREEN_WIDTH - 200, 20))

    pygame.display.update()
    FramePerSec.tick(60)