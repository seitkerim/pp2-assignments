import pygame
import sys

pygame.init()

# ── Размер окна ──────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# ── Цвета ────────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GRAY   = (200, 200, 200)

# Палитра цветов внизу экрана
PALETTE = [
    (  0,   0,   0),   # чёрный
    (255, 255, 255),   # белый
    (255,   0,   0),   # красный
    (  0, 200,   0),   # зелёный
    (  0,   0, 255),   # синий
    (255, 255,   0),   # жёлтый
    (255, 128,   0),   # оранжевый
    (180,   0, 255),   # фиолетовый
    (  0, 200, 255),   # голубой
    (255,   0, 180),   # розовый
]

# ── Переменные состояния ──────────────────────────────────────────────────────
color      = BLACK    # текущий цвет
tool       = "pen"    # текущий инструмент: pen, rect, circle, eraser
size       = 5        # размер кисти
drawing    = False    # зажата ли мышь
start_pos  = None     # начальная точка (для фигур)
last_pos   = None     # предыдущая точка (для пера)

# ── Холст ─────────────────────────────────────────────────────────────────────
# Рисуем на отдельной поверхности, чтобы панель не стиралась
PANEL_H = 60
canvas = pygame.Surface((WIDTH, HEIGHT - PANEL_H))
canvas.fill(WHITE)

# ── Шрифт ─────────────────────────────────────────────────────────────────────
font = pygame.font.SysFont("Arial", 16)


def draw_panel():
    """Рисует нижнюю панель с инструментами и цветами."""

    # Фон панели
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - PANEL_H, WIDTH, PANEL_H))
    pygame.draw.line(screen, BLACK, (0, HEIGHT - PANEL_H), (WIDTH, HEIGHT - PANEL_H), 2)

    # ── Кнопки инструментов ───────────────────────────────────────────────────
    tools = ["pen", "rect", "circle", "eraser"]
    for i, t in enumerate(tools):
        x = 10 + i * 80
        y = HEIGHT - PANEL_H + 10
        btn_color = (100, 149, 237) if tool == t else (170, 170, 170)
        pygame.draw.rect(screen, btn_color, (x, y, 70, 30), border_radius=5)
        txt = font.render(t, True, BLACK)
        screen.blit(txt, (x + 5, y + 7))

    # ── Палитра цветов ────────────────────────────────────────────────────────
    for i, c in enumerate(PALETTE):
        x = 350 + i * 35
        y = HEIGHT - PANEL_H + 10
        pygame.draw.rect(screen, c, (x, y, 30, 30))
        if c == color:
            pygame.draw.rect(screen, BLACK, (x, y, 30, 30), 3)
        else:
            pygame.draw.rect(screen, BLACK, (x, y, 30, 30), 1)

    # ── Кнопка Clear ─────────────────────────────────────────────────────────
    pygame.draw.rect(screen, (220, 80, 80), (810, HEIGHT - PANEL_H + 10, 70, 30), border_radius=5)
    txt = font.render("Clear", True, WHITE)
    screen.blit(txt, (820, HEIGHT - PANEL_H + 17))


def get_tool_btn(mx, my):
    """Возвращает название инструмента если кликнули на его кнопку."""
    tools = ["pen", "rect", "circle", "eraser"]
    for i, t in enumerate(tools):
        x = 10 + i * 80
        y = HEIGHT - PANEL_H + 10
        if x <= mx <= x + 70 and y <= my <= y + 30:
            return t
    return None


def get_palette_color(mx, my):
    """Возвращает цвет если кликнули на палитру."""
    for i, c in enumerate(PALETTE):
        x = 350 + i * 35
        y = HEIGHT - PANEL_H + 10
        if x <= mx <= x + 30 and y <= my <= y + 30:
            return c
    return None


def draw_preview(surface, s, e):
    """Рисует предпросмотр фигуры пока тащим мышь."""
    if tool == "rect":
        x = min(s[0], e[0])
        y = min(s[1], e[1])
        w = abs(e[0] - s[0])
        h = abs(e[1] - s[1])
        pygame.draw.rect(surface, color, (x, y, w, h), size)

    elif tool == "circle":
        cx = (s[0] + e[0]) // 2
        cy = (s[1] + e[1]) // 2
        rx = abs(e[0] - s[0]) // 2
        ry = abs(e[1] - s[1]) // 2
        if rx > 1 and ry > 1:
            pygame.draw.ellipse(surface, color, (cx - rx, cy - ry, rx * 2, ry * 2), size)


# ── Главный цикл ──────────────────────────────────────────────────────────────
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Клик по панели снизу
            if my >= HEIGHT - PANEL_H:
                t = get_tool_btn(mx, my)
                if t:
                    tool = t

                c = get_palette_color(mx, my)
                if c:
                    color = c
                    tool = "pen"

                # Кнопка Clear
                if 810 <= mx <= 880 and HEIGHT - PANEL_H + 10 <= my <= HEIGHT - PANEL_H + 40:
                    canvas.fill(WHITE)

            # Клик по холсту
            else:
                drawing   = True
                start_pos = (mx, my)
                last_pos  = (mx, my)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                mx, my = event.pos
                if tool in ("rect", "circle"):
                    draw_preview(canvas, start_pos, (mx, my))
            drawing   = False
            start_pos = None
            last_pos  = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                mx, my = event.pos
                my = min(my, HEIGHT - PANEL_H - 1)

                if tool == "pen":
                    pygame.draw.line(canvas, color, last_pos, (mx, my), size)
                    last_pos = (mx, my)

                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, (mx, my), 15)

    # ── Рисуем кадр ───────────────────────────────────────────────────────────

    # 1. Холст
    screen.blit(canvas, (0, 0))

    # 2. Призрак фигуры во время перетаскивания
    if drawing and tool in ("rect", "circle") and start_pos:
        mx, my = pygame.mouse.get_pos()
        temp = canvas.copy()
        draw_preview(temp, start_pos, (mx, my))
        screen.blit(temp, (0, 0))

    # 3. Панель
    draw_panel()

    pygame.display.flip()
    clock.tick(60)