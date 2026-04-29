import pygame
import sys
import math

pygame.init()

# ── Настройки окна ────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 900, 600
PANEL_H = 60          # высота нижней панели
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# ── Цвета ─────────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GRAY   = (200, 200, 200)
D_GRAY = (120, 120, 120)

# Палитра цветов
PALETTE = [
    (  0,   0,   0), (255, 255, 255), (255,   0,   0), (  0, 200,   0),
    (  0,   0, 255), (255, 255,   0), (255, 128,   0), (180,   0, 255),
    (  0, 200, 255), (255,   0, 180),
]

# ── Состояние ─────────────────────────────────────────────────────────────────
color     = BLACK    # текущий цвет
tool      = "pen"    # текущий инструмент
size      = 5        # толщина линии / кисти
drawing   = False    # зажата ли мышь
start_pos = None     # начальная точка фигуры
last_pos  = None     # предыдущая точка (для пера)

# ── Холст ─────────────────────────────────────────────────────────────────────
canvas = pygame.Surface((WIDTH, HEIGHT - PANEL_H))
canvas.fill(WHITE)

# ── Шрифт ─────────────────────────────────────────────────────────────────────
font = pygame.font.SysFont("Arial", 14)


# ── Функции рисования фигур ───────────────────────────────────────────────────

def draw_rect(surface, s, e, clr, thickness):
    """Прямоугольник по двум точкам."""
    x = min(s[0], e[0])
    y = min(s[1], e[1])
    w = abs(e[0] - s[0])
    h = abs(e[1] - s[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surface, clr, (x, y, w, h), thickness)


def draw_square(surface, s, e, clr, thickness):
    """Квадрат — берём меньшую из сторон чтобы стороны были равны."""
    side = min(abs(e[0] - s[0]), abs(e[1] - s[1]))
    # Направление по знаку смещения
    dx = 1 if e[0] >= s[0] else -1          
    dy = 1 if e[1] >= s[1] else -1
    x = s[0] if dx > 0 else s[0] - side
    y = s[1] if dy > 0 else s[1] - side
    if side > 0:
        pygame.draw.rect(surface, clr, (x, y, side, side), thickness)


def draw_circle(surface, s, e, clr, thickness):
    """Эллипс вписанный в прямоугольник между двумя точками."""
    x  = min(s[0], e[0])
    y  = min(s[1], e[1])
    w  = abs(e[0] - s[0])
    h  = abs(e[1] - s[1])
    if w > 1 and h > 1:
        pygame.draw.ellipse(surface, clr, (x, y, w, h), thickness)


def draw_right_triangle(surface, s, e, clr, thickness):
    """Прямоугольный треугольник.
       Прямой угол — в точке s (левый нижний).
       Вершины: s, (e[0], s[1]), e  — но подгоняем под направление тащения.
    """
    # Всегда: правый угол снизу-слева относительно направления
    p1 = s                   # прямой угол
    p2 = (e[0], s[1])        # горизонтальный катет
    p3 = e                   # конец гипотенузы
    pygame.draw.polygon(surface, clr, [p1, p2, p3], thickness)


def draw_equilateral_triangle(surface, s, e, clr, thickness):
    """Равносторонний треугольник.
       Основание горизонтальное между s и (e[0], s[1]).
       Вершина вычисляется через высоту = сторона * sqrt(3)/2.
    """
    base  = abs(e[0] - s[0])
    if base < 2:
        return
    # Левый и правый концы основания
    left  = min(s[0], e[0])
    right = max(s[0], e[0])
    base_y = s[1]
    # Высота равностороннего треугольника
    h = int(base * math.sqrt(3) / 2)
    # Вершина — вверх или вниз в зависимости от направления
    direction = -1 if e[1] <= s[1] else 1
    apex = ((left + right) // 2, base_y + direction * h)
    p1 = (left, base_y)
    p2 = (right, base_y)
    pygame.draw.polygon(surface, clr, [p1, p2, apex], thickness)


def draw_rhombus(surface, s, e, clr, thickness):
    """Ромб вписанный в прямоугольник между s и e.
       4 точки: верх, право, низ, лево.
    """
    x  = min(s[0], e[0])
    y  = min(s[1], e[1])
    w  = abs(e[0] - s[0])
    h  = abs(e[1] - s[1])
    if w < 2 or h < 2:
        return
    top    = (x + w // 2, y)
    right  = (x + w,      y + h // 2)
    bottom = (x + w // 2, y + h)
    left   = (x,          y + h // 2)
    pygame.draw.polygon(surface, clr, [top, right, bottom, left], thickness)


# Словарь: название инструмента → функция рисования
SHAPE_FUNCS = {
    "rect":     draw_rect,
    "square":   draw_square,
    "circle":   draw_circle,
    "r_tri":    draw_right_triangle,
    "eq_tri":   draw_equilateral_triangle,
    "rhombus":  draw_rhombus,
}

# Все инструменты (название для кнопки)
TOOLS = [
    ("pen",     "Pen"),
    ("eraser",  "Eraser"),
    ("rect",    "Rect"),
    ("square",  "Square"),
    ("circle",  "Circle"),
    ("r_tri",   "R.Tri"),
    ("eq_tri",  "Eq.Tri"),
    ("rhombus", "Rhombus"),
]


# ── Панель ────────────────────────────────────────────────────────────────────
def draw_panel():
    """Рисует нижнюю панель: инструменты, палитра, Clear."""
    y0 = HEIGHT - PANEL_H
    pygame.draw.rect(screen, GRAY, (0, y0, WIDTH, PANEL_H))
    pygame.draw.line(screen, BLACK, (0, y0), (WIDTH, y0), 2)

    # Кнопки инструментов
    for i, (tid, tname) in enumerate(TOOLS):
        x   = 5 + i * 72
        btn = pygame.Rect(x, y0 + 8, 68, 28)
        clr = (100, 149, 237) if tool == tid else (160, 160, 160)
        pygame.draw.rect(screen, clr, btn, border_radius=4)
        txt = font.render(tname, True, BLACK)
        screen.blit(txt, (x + (68 - txt.get_width()) // 2, y0 + 15))

    # Палитра
    px = 5 + len(TOOLS) * 72 + 8
    for i, c in enumerate(PALETTE):
        rx = px + i * 28
        ry = y0 + 10
        pygame.draw.rect(screen, c, (rx, ry, 24, 24))
        if c == color:
            pygame.draw.rect(screen, BLACK, (rx, ry, 24, 24), 3)
        else:
            pygame.draw.rect(screen, D_GRAY, (rx, ry, 24, 24), 1)

    # Кнопка Clear
    pygame.draw.rect(screen, (210, 60, 60), (WIDTH - 68, y0 + 10, 62, 28), border_radius=4)
    txt = font.render("Clear", True, WHITE)
    screen.blit(txt, (WIDTH - 68 + (62 - txt.get_width()) // 2, y0 + 17))


def get_clicked_tool(mx, my):
    """Возвращает id инструмента если кликнули на его кнопку."""
    y0 = HEIGHT - PANEL_H
    for i, (tid, _) in enumerate(TOOLS):
        x = 5 + i * 72
        if x <= mx <= x + 68 and y0 + 8 <= my <= y0 + 36:
            return tid
    return None


def get_clicked_color(mx, my):
    """Возвращает цвет если кликнули на палитру."""
    y0 = HEIGHT - PANEL_H
    px = 5 + len(TOOLS) * 72 + 8
    for i, c in enumerate(PALETTE):
        rx = px + i * 28
        if rx <= mx <= rx + 24 and y0 + 10 <= my <= y0 + 34:
            return c
    return None


def draw_preview(surface, s, e):
    """Рисует призрак фигуры пока тащим мышь."""
    if tool in SHAPE_FUNCS:
        SHAPE_FUNCS[tool](surface, s, e, color, size)


# ── Главный цикл ──────────────────────────────────────────────────────────────
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Клик по панели
            if my >= HEIGHT - PANEL_H:
                # Инструмент?
                t = get_clicked_tool(mx, my)
                if t:
                    tool = t

                # Цвет?
                c = get_clicked_color(mx, my)
                if c:
                    color = c
                    if tool == "eraser":
                        tool = "pen"

                # Clear?
                if WIDTH - 68 <= mx <= WIDTH - 6 and HEIGHT - PANEL_H + 10 <= my <= HEIGHT - PANEL_H + 38:
                    canvas.fill(WHITE)

            # Клик по холсту — начинаем рисовать
            else:
                drawing   = True
                start_pos = (mx, my)
                last_pos  = (mx, my)
        elif event.type == pygame.MOUSEBUTTONUP:
            # Фиксируем фигуру на холсте
            if drawing and start_pos:
                mx, my = event.pos
                my = min(my, HEIGHT - PANEL_H - 1)
                if tool in SHAPE_FUNCS:
                    draw_preview(canvas, start_pos, (mx, my))
            drawing   = False
            start_pos = None
            last_pos  = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                mx, my = event.pos
                my = min(my, HEIGHT - PANEL_H - 1)
                if tool == "pen":
                    # Рисуем линию от предыдущей точки к текущей
                    pygame.draw.line(canvas, color, last_pos, (mx, my), size)
                    last_pos = (mx, my)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, (mx, my), 15)
    # ── Рисуем кадр ───────────────────────────────────────────────────────────
    # 1. Холст
    screen.blit(canvas, (0, 0))
    # 2. Призрак фигуры во время перетаскивания
    if drawing and tool in SHAPE_FUNCS and start_pos:
        mx, my = pygame.mouse.get_pos()
        my = min(my, HEIGHT - PANEL_H - 1)
        temp = canvas.copy()
        draw_preview(temp, start_pos, (mx, my))
        screen.blit(temp, (0, 0))
    # 3. Панель
    draw_panel()
    pygame.display.flip()
    clock.tick(60)