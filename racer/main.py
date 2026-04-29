import pygame
import sys
import random
import os
from pygame.locals import *

pygame.init()

# ── ПУТИ К ФАЙЛАМ ─────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# ── FPS (скорость игры) ───────────────────────
FPS = 60
FramePerSec = pygame.time.Clock()

# ── РАЗМЕР ОКНА ───────────────────────────────
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# ── ЦВЕТА ──────────────────────────────────────
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# ── СОЗДАНИЕ ОКНА ─────────────────────────────
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# ── ШРИФТ ДЛЯ ТЕКСТА ──────────────────────────
font = pygame.font.SysFont("Verdana", 30)

# ── ИГРОВЫЕ ПЕРЕМЕННЫЕ ────────────────────────
score = 0
coins_collected = 0
speed = 5


# ───────────────────────────────────────────────
# ENEMY (ВРАГ) - движение вниз + перерождение
# ───────────────────────────────────────────────
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # загрузка картинки врага
        img = pygame.image.load(os.path.join(IMAGES_DIR, "enemy.png"))
        self.image = pygame.transform.smoothscale(img, (90, 140))

        # прямоугольник (позиция + столкновения)
        self.rect = self.image.get_rect()

        self.reset()

    # ── СБРОС ВРАГА ВВЕРХ ЭКРАНА ──
    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -150

    # ── ДВИЖЕНИЕ ВРАГА ВНИЗ ──
    def move(self):
        global score, speed

        self.rect.move_ip(0, speed)

        # если враг ушёл за экран
        if self.rect.top > SCREEN_HEIGHT:
            score += 1      # +1 очко
            speed += 0.2    # увеличение скорости
            self.reset()

    # ── ОТРИСОВКА ВРАГА ──
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ───────────────────────────────────────────────
# PLAYER (ИГРОК) - управление клавиатурой
# ───────────────────────────────────────────────
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        img = pygame.image.load(os.path.join(IMAGES_DIR, "car.png"))
        self.image = pygame.transform.smoothscale(img, (90, 140))

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)

    # ── УПРАВЛЕНИЕ (ЛЕВО / ПРАВО) ──
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-7, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(7, 0)

    # ── ОТРИСОВКА ИГРОКА ──
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ───────────────────────────────────────────────
# COIN (МОНЕТА) - сбор бонусов
# ───────────────────────────────────────────────
class Coin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        img = pygame.image.load(os.path.join(IMAGES_DIR, "coin.png"))
        self.image = pygame.transform.smoothscale(img, (40, 40))

        self.rect = self.image.get_rect()
        self.reset()

    # ── СБРОС МОНЕТЫ ──
    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300, -50)

    # ── ДВИЖЕНИЕ МОНЕТЫ ВНИЗ ──
    def move(self):
        self.rect.move_ip(0, speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    # ── ОТРИСОВКА МОНЕТЫ ──
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ───────────────────────────────────────────────
# СОЗДАНИЕ ОБЪЕКТОВ ИГРЫ
# ───────────────────────────────────────────────
P1 = Player()
E1 = Enemy()
C1 = Coin()


# ───────────────────────────────────────────────
# ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
# ───────────────────────────────────────────────
while True:

    # ── ОБРАБОТКА СОБЫТИЙ (клавиатура / выход)
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # ── ОБНОВЛЕНИЕ ИГРОВОЙ ЛОГИКИ
    P1.update()   # движение игрока
    E1.move()     # движение врага
    C1.move()     # движение монеты

    # ── СТОЛКНОВЕНИЕ С ВРАГОМ (GAME OVER)
    if pygame.sprite.collide_rect(P1, E1):
        text = font.render("GAME OVER", True, BLACK)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        DISPLAYSURF.blit(text, rect)
        pygame.display.update()

        pygame.time.delay(2000)

        pygame.quit()
        sys.exit()

    # ── СТОЛКНОВЕНИЕ С МОНЕТОЙ (СБОР)
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += 1
        C1.reset()

    # ── РИСОВАНИЕ ЭКРАНА
    DISPLAYSURF.fill(GRAY)

    P1.draw(DISPLAYSURF)  # игрок
    E1.draw(DISPLAYSURF)  # враг
    C1.draw(DISPLAYSURF)  # монета

    # ── ТЕКСТ НА ЭКРАНЕ (СЧЁТ / МОНЕТЫ)
    score_text = font.render(f"Score: {score}", True, WHITE)
    coin_text = font.render(f"Coins: {coins_collected}", True, WHITE)

    DISPLAYSURF.blit(score_text, (20, 20))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 200, 20))

    # ── ОБНОВЛЕНИЕ ЭКРАНА
    pygame.display.update()
    FramePerSec.tick(FPS)