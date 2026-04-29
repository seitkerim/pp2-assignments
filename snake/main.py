import pygame
import sys
import random
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
font = pygame.font.SysFont("Verdana", 24)
font_big = pygame.font.SysFont("Verdana", 36, bold=True)

# сбрасывает все параметры игры до начальных значений и возвращает их
def init_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    score = 0
    level = 1
    foods_to_next_level = 3
    speed = 5
    food = generate_food(snake)
    return snake, direction, score, level, foods_to_next_level, speed, food

# генерирует случайную позицию еды, которая не совпадает с телом змейки
def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

# рисует каждый блок змейки на экране
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE))

# рисует еду на экране
def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

# проверяет столкновение головы змейки со стеной
def check_wall_collision(head):
    return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT

# проверяет столкновение головы змейки с её телом
def check_self_collision(head, snake):
    return head in snake[1:]

# показывает экран смерти и ждёт нажатия R (рестарт) или Q (выход)
def show_game_over(score, level):
    while True:
        screen.fill(BLACK)
        text1 = font_big.render("GAME OVER", True, RED)
        text2 = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        text3 = font.render("R - перезапустить  |  Q - выйти", True, WHITE)
        # выравниваем текст по центру экрана
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 70))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))
        screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# внешний цикл — перезапускает игру после смерти
while True:
    snake, direction, score, level, foods_to_next_level, speed, food = init_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # меняем направление только если оно не противоположное текущему
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1]) # вычисляем новую позицию головы
        if check_wall_collision(new_head) or check_self_collision(new_head, snake):
            running = False
            break
        snake.insert(0, new_head) # добавляем новую голову в начало змейки
        if new_head == food:
            score += 1
            foods_to_next_level -= 1
            food = generate_food(snake)
        else:
            snake.pop() # убираем хвост если еда не съедена (змейка движется)
        if foods_to_next_level == 0: # повышаем уровень каждые 3 съеденные еды
            level += 1
            foods_to_next_level = 3
            speed += 2
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 40))
        pygame.display.update()
        clock.tick(speed) # ограничиваем скорость игры
    show_game_over(score, level)