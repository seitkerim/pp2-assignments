import pygame
import sys
import random

pygame.init()

# ── Настройки окна ────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
FPS = 60

# ── Цвета ─────────────────────────────────────────────────────────────────────
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (100, 100, 100)
DARK_GRAY  = ( 50,  50,  50)
RED        = (220,  50,  50)
BLUE       = ( 50, 100, 220)
YELLOW     = (255, 220,   0)
GREEN      = ( 50, 200,  50)
ROAD_CLR   = ( 60,  60,  60)
LINE_CLR   = (200, 200,   0)
GRASS_CLR  = ( 34, 139,  34)

font_big   = pygame.font.SysFont("Arial", 42, bold=True)
font_med   = pygame.font.SysFont("Arial", 24, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

# ── Дорога ────────────────────────────────────────────────────────────────────
ROAD_LEFT  = 80     # левый край дороги
ROAD_RIGHT = 420    # правый край дороги
ROAD_W     = ROAD_RIGHT - ROAD_LEFT

# Полосы дороги (3 полосы)
LANES = [
    ROAD_LEFT + ROAD_W // 6,           # левая полоса
    ROAD_LEFT + ROAD_W // 2,           # средняя полоса
    ROAD_LEFT + ROAD_W * 5 // 6,       # правая полоса
]

# ── Класс: машина игрока ───────────────────────────────────────────────────────
class PlayerCar:
    def __init__(self):
        self.w = 50
        self.h = 80
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 120
        self.speed = 5         # скорость движения влево/вправо

    def draw(self, screen):
        # Кузов
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.w, self.h), border_radius=8)
        # Лобовое стекло
        pygame.draw.rect(screen, (150, 200, 255), (self.x + 8, self.y + 10, self.w - 16, 20), border_radius=4)
        # Заднее стекло
        pygame.draw.rect(screen, (150, 200, 255), (self.x + 8, self.y + self.h - 30, self.w - 16, 15), border_radius=4)
        # Колёса
        pygame.draw.rect(screen, BLACK, (self.x - 8,       self.y + 10, 10, 20), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.w - 2, self.y + 10, 10, 20), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x - 8,       self.y + self.h - 30, 10, 20), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.w - 2, self.y + self.h - 30, 10, 20), border_radius=3)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self, keys):
        if keys[pygame.K_LEFT]  and self.x > ROAD_LEFT + 5:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.w < ROAD_RIGHT - 5:
            self.x += self.speed


# ── Класс: машина-противник ───────────────────────────────────────────────────
class EnemyCar:
    COLORS = [RED, (220, 100, 0), (180, 0, 180), (0, 180, 180)]

    def __init__(self, speed):
        self.w = 50
        self.h = 80
        lane = random.choice(LANES)
        self.x = lane - self.w // 2
        self.y = -self.h                    # начинает выше экрана
        self.speed = speed
        self.color = random.choice(self.COLORS)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), border_radius=8)
        pygame.draw.rect(screen, (255, 200, 150), (self.x + 8, self.y + 10, self.w - 16, 20), border_radius=4)
        pygame.draw.rect(screen, (255, 200, 150), (self.x + 8, self.y + self.h - 30, self.w - 16, 15), border_radius=4)
        pygame.draw.rect(screen, BLACK, (self.x - 8,       self.y + 10, 10, 20), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.w - 2, self.y + 10, 10, 20), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x - 8,       self.y + self.h - 30, 10, 20), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.w - 2, self.y + self.h - 30, 10, 20), border_radius=3)

    def update(self):
        self.y += self.speed   # едет вниз

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def is_off_screen(self):
        return self.y > HEIGHT


# ── Класс: монета ─────────────────────────────────────────────────────────────
class Coin:
    def __init__(self, speed):
        lane = random.choice(LANES)
        self.x = lane              # центр монеты
        self.y = -20
        self.r = 14                # радиус
        self.speed = speed

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.r)
        pygame.draw.circle(screen, (200, 160, 0), (self.x, self.y), self.r, 2)
        # Знак $ внутри
        txt = font_small.render("$", True, (150, 100, 0))
        screen.blit(txt, (self.x - txt.get_width() // 2, self.y - txt.get_height() // 2))

    def update(self):
        self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def is_off_screen(self):
        return self.y > HEIGHT


# ── Рисование дороги ──────────────────────────────────────────────────────────
road_line_y = 0   # анимация дорожной разметки (глобальная)

def draw_road():
    global road_line_y

    # Трава по бокам
    screen.fill(GRASS_CLR)

    # Дорога
    pygame.draw.rect(screen, ROAD_CLR, (ROAD_LEFT, 0, ROAD_W, HEIGHT))

    # Края дороги (белые полосы)
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT, 0, 6, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 6, 0, 6, HEIGHT))

    # Разделительные пунктирные линии (анимированные)
    road_line_y = (road_line_y + 5) % 80    # двигаются вниз
    for lane_x in [ROAD_LEFT + ROAD_W // 3, ROAD_LEFT + ROAD_W * 2 // 3]:
        y = -80 + road_line_y
        while y < HEIGHT:
            pygame.draw.rect(screen, LINE_CLR, (lane_x - 3, y, 6, 40))
            y += 80


# ── Экраны ────────────────────────────────────────────────────────────────────
def show_start_screen():
    screen.fill(BLACK)
    t1 = font_big.render("RACER", True, YELLOW)
    t2 = font_med.render("Press SPACE to start", True, WHITE)
    t3 = font_small.render("Use LEFT / RIGHT arrows to drive", True, GRAY)
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 200))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 300))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 350))
    pygame.display.flip()
    wait_for_key(pygame.K_SPACE)


def show_game_over(score, coins):
    screen.fill(BLACK)
    t1 = font_big.render("GAME OVER", True, RED)
    t2 = font_med.render(f"Score: {score}   Coins: {coins}", True, WHITE)
    t3 = font_small.render("Press SPACE to play again", True, GRAY)
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 220))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 300))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 360))
    pygame.display.flip()
    wait_for_key(pygame.K_SPACE)


def wait_for_key(key):
    """Ждёт нажатия конкретной клавиши."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == key:
                return


# ── Основная игра ─────────────────────────────────────────────────────────────
def run_game():
    player = PlayerCar()
    enemies = []
    coins   = []

    score      = 0       # очки (за время выживания)
    coin_count = 0       # собранные монеты

    enemy_speed  = 5     # начальная скорость врагов
    enemy_timer  = 0     # таймер появления врагов
    enemy_delay  = 90    # каждые 90 кадров новый враг

    coin_timer   = 0     # таймер появления монет
    coin_delay   = 120   # каждые 120 кадров новая монета

    running = True
    while running:

        clock.tick(FPS)

        # ── События ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # ── Управление игроком ────────────────────────────────────────────────
        keys = pygame.key.get_pressed()
        player.move(keys)

        # ── Счёт растёт со временем ───────────────────────────────────────────
        score += 1

        # ── Постепенно увеличиваем скорость ───────────────────────────────────
        enemy_speed = 5 + score // 300   # каждые 5 секунд +1 к скорости

        # ── Спавн врагов ──────────────────────────────────────────────────────
        enemy_timer += 1
        if enemy_timer >= enemy_delay:
            enemies.append(EnemyCar(enemy_speed))
            enemy_timer = 0
            # Со временем враги появляются чаще
            enemy_delay = max(40, 90 - score // 200)

        # ── Спавн монет ───────────────────────────────────────────────────────
        coin_timer += 1
        if coin_timer >= coin_delay:
            coins.append(Coin(enemy_speed))
            coin_timer = 0

        # ── Обновляем врагов ──────────────────────────────────────────────────
        for enemy in enemies:
            enemy.update()
        enemies = [e for e in enemies if not e.is_off_screen()]

        # ── Обновляем монеты ──────────────────────────────────────────────────
        for coin in coins:
            coin.update()
        coins = [c for c in coins if not c.is_off_screen()]

        # ── Проверка столкновения с врагом ────────────────────────────────────
        for enemy in enemies:
            if player.get_rect().colliderect(enemy.get_rect()):
                return score, coin_count   # конец игры

        # ── Проверка сбора монет ──────────────────────────────────────────────
        collected = []
        for coin in coins:
            if player.get_rect().colliderect(coin.get_rect()):
                coin_count += 1
                collected.append(coin)
        coins = [c for c in coins if c not in collected]

        # ── Рисуем ────────────────────────────────────────────────────────────
        draw_road()

        for enemy in enemies:
            enemy.draw(screen)

        for coin in coins:
            coin.draw(screen)

        player.draw(screen)

        # Счёт в правом верхнем углу
        score_txt = font_med.render(f"Score: {score // 10}", True, WHITE)
        coins_txt = font_med.render(f"Coins: {coin_count}", True, YELLOW)
        screen.blit(score_txt, (10, 10))
        screen.blit(coins_txt, (WIDTH - coins_txt.get_width() - 10, 10))

        pygame.display.flip()


# ── Запуск ────────────────────────────────────────────────────────────────────
show_start_screen()

while True:
    final_score, final_coins = run_game()
    show_game_over(final_score // 10, final_coins)