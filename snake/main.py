import pygame
import sys
import random

pygame.init()

# ── Настройки ─────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 600, 600
CELL = 30                        # размер одной клетки
COLS = WIDTH // CELL             # количество колонок
ROWS = HEIGHT // CELL            # количество строк

screen = pygame.display.set_mode((WIDTH, HEIGHT + 60))  # +60 для панели счёта
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# ── Цвета ─────────────────────────────────────────────────────────────────────
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = ( 50, 200,  50)
DARK_GREEN = ( 30, 130,  30)
RED        = (220,  50,  50)
GRAY       = ( 40,  40,  40)
PANEL_CLR  = ( 20,  20,  20)
YELLOW     = (255, 220,   0)

font_big   = pygame.font.SysFont("Arial", 36, bold=True)
font_small = pygame.font.SysFont("Arial", 20)


# ── Вспомогательная: клетка → пиксели ────────────────────────────────────────
def cell_rect(col, row):
    """Возвращает pygame.Rect для клетки (col, row)."""
    return pygame.Rect(col * CELL, row * CELL, CELL - 1, CELL - 1)


# ── Генерация еды ─────────────────────────────────────────────────────────────
def spawn_food(snake_body):
    """Ставит еду в случайную клетку, не занятую змейкой и не на стене."""
    while True:
        col = random.randint(1, COLS - 2)   # 1..18 — не попадёт на стену
        row = random.randint(1, ROWS - 2)
        if (col, row) not in snake_body:    # не на змейке
            return (col, row)


# ── Рисование стен ────────────────────────────────────────────────────────────
def draw_walls():
    """Рисует стену по периметру поля."""
    for col in range(COLS):
        pygame.draw.rect(screen, GRAY, cell_rect(col, 0))           # верх
        pygame.draw.rect(screen, GRAY, cell_rect(col, ROWS - 1))    # низ
    for row in range(ROWS):
        pygame.draw.rect(screen, GRAY, cell_rect(0, row))           # лево
        pygame.draw.rect(screen, GRAY, cell_rect(COLS - 1, row))    # право


# ── Рисование панели счёта ────────────────────────────────────────────────────
def draw_panel(score, level):
    y = HEIGHT
    pygame.draw.rect(screen, PANEL_CLR, (0, y, WIDTH, 60))
    pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y), 1)

    score_txt = font_small.render(f"Score: {score}", True, WHITE)
    level_txt = font_small.render(f"Level: {level}", True, YELLOW)
    speed_txt = font_small.render(f"Speed: {6 + (level - 1) * 2}", True, WHITE)

    screen.blit(score_txt, (20, y + 18))
    screen.blit(level_txt, (WIDTH // 2 - 40, y + 18))
    screen.blit(speed_txt, (WIDTH - 150, y + 18))


# ── Экран Game Over / Level Up ────────────────────────────────────────────────
def show_message(title, subtitle):
    """Показывает сообщение поверх экрана и ждёт нажатия клавиши."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    t1 = font_big.render(title, True, WHITE)
    t2 = font_small.render(subtitle, True, GRAY)

    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

    # Ждём нажатия любой клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# ── Сброс игры ────────────────────────────────────────────────────────────────
def reset_game():
    """Возвращает начальное состояние змейки и счёт."""
    snake = [(COLS // 2, ROWS // 2)]   # змейка из одной клетки в центре
    direction = (1, 0)                 # движется вправо
    score = 0
    level = 1
    food = spawn_food(snake)
    return snake, direction, score, level, food


# ── Старт ─────────────────────────────────────────────────────────────────────
snake, direction, score, level, food = reset_game()
next_dir = direction    # направление, которое выберет игрок (применяем на следующем шаге)
FPS = 6                 # скорость (кадров в секунду = шагов в секунду)

# ── Главный цикл ──────────────────────────────────────────────────────────────
running = True
while running:

    clock.tick(FPS)

    # ── События ───────────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Меняем направление, но нельзя повернуть на 180°
            if event.key == pygame.K_UP    and direction != (0, 1):
                next_dir = (0, -1)
            if event.key == pygame.K_DOWN  and direction != (0, -1):
                next_dir = (0, 1)
            if event.key == pygame.K_LEFT  and direction != (1, 0):
                next_dir = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_dir = (1, 0)

    # ── Движение змейки ───────────────────────────────────────────────────────
    direction = next_dir
    head_col = snake[0][0] + direction[0]
    head_row = snake[0][1] + direction[1]
    new_head = (head_col, head_row)

    # ── Проверка столкновений ─────────────────────────────────────────────────

    # Удар о стену (клетки 0 и COLS-1 / ROWS-1)
    if head_col == 0 or head_col == COLS - 1 or head_row == 0 or head_row == ROWS - 1:
        show_message("GAME OVER", "Press any key to restart")
        snake, direction, score, level, food = reset_game()
        next_dir = direction
        FPS = 6
        continue

    # Укусила себя
    if new_head in snake:
        show_message("GAME OVER", "Press any key to restart")
        snake, direction, score, level, food = reset_game()
        next_dir = direction
        FPS = 6
        continue

    # ── Добавляем новую голову ────────────────────────────────────────────────
    snake.insert(0, new_head)

    # ── Съела еду? ────────────────────────────────────────────────────────────
    if new_head == food:
        score += 1
        food = spawn_food(snake)   # хвост НЕ удаляем — змейка растёт

        # ── Переход на новый уровень каждые 3 очка ────────────────────────────
        if score % 3 == 0:
            level += 1
            FPS = 6 + (level - 1) * 2   # увеличиваем скорость
            show_message(f"LEVEL {level}!", "Press any key to continue")
    else:
        snake.pop()   # убираем хвост — змейка движется

    # ── Рисуем ────────────────────────────────────────────────────────────────
    screen.fill(BLACK)

    # Сетка (необязательно, но красиво)
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(screen, (15, 15, 15), cell_rect(col, row))

    # Стены
    draw_walls()

    # Еда
    pygame.draw.rect(screen, RED, cell_rect(food[0], food[1]))

    # Змейка
    for i, (col, row) in enumerate(snake):
        c = GREEN if i > 0 else DARK_GREEN   # голова темнее
        pygame.draw.rect(screen, c, cell_rect(col, row))

    # Панель счёта
    draw_panel(score, level)

    pygame.display.flip()