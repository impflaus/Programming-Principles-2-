import pygame
import sys
import math

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Paint with More Shapes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

ERASER_COLOR = WHITE

# Variables
clock = pygame.time.Clock()
running = True
drawing = False
start_pos = None
draw_mode = 'line'
current_color = BLACK
brush_size = 3

# Canvas setup
canvas = pygame.Surface((WIDTH, HEIGHT - 50))
canvas.fill(WHITE)

# UI rendering
def draw_ui():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, 50))

    # Color boxes
    pygame.draw.rect(screen, RED,   (10, 10, 30, 30))
    pygame.draw.rect(screen, GREEN, (50, 10, 30, 30))
    pygame.draw.rect(screen, BLUE,  (90, 10, 30, 30))
    pygame.draw.rect(screen, BLACK, (130, 10, 30, 30))
    pygame.draw.rect(screen, WHITE, (170, 10, 30, 30))  # White for erasing color

    # Shape tools
    buttons = {
        'Rect': ('rect', 220),
        'Circle': ('circle', 290),
        'Line': ('line', 360),
        'Square': ('square', 430),
        'Right': ('right_triangle', 500),
        'Equi△': ('equilateral_triangle', 570),
        'Rhomb': ('rhombus', 660),
    }

    font = pygame.font.SysFont(None, 20)
    for label, (mode, x) in buttons.items():
        pygame.draw.rect(screen, (100, 100, 100), (x, 10, 60, 30))
        screen.blit(font.render(label, True, WHITE), (x + 5, 18))

    # Eraser button in top right corner
    pygame.draw.rect(screen, (100, 100, 100), (WIDTH - 50, 10, 40, 30))
    screen.blit(font.render("Erase", True, WHITE), (WIDTH - 48, 18))


# Game loop
while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 50))
    draw_ui()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mx, my = mouse_x, mouse_y - 50

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_y < 50:
                # Color selection
                if pygame.Rect(10, 10, 30, 30).collidepoint(event.pos): current_color = RED
                elif pygame.Rect(50, 10, 30, 30).collidepoint(event.pos): current_color = GREEN
                elif pygame.Rect(90, 10, 30, 30).collidepoint(event.pos): current_color = BLUE
                elif pygame.Rect(130, 10, 30, 30).collidepoint(event.pos): current_color = BLACK
                elif pygame.Rect(170, 10, 30, 30).collidepoint(event.pos): current_color = WHITE

                # Tool selection
                if pygame.Rect(WIDTH - 50, 10, 40, 30).collidepoint(event.pos):
                    draw_mode = 'eraser'
                else:
                    tool_buttons = {
                        (220, 'rect'), (290, 'circle'), (360, 'line'),
                        (430, 'square'), (500, 'right_triangle'),
                        (570, 'equilateral_triangle'), (660, 'rhombus')
                    }
                    for x, mode in tool_buttons:
                        if pygame.Rect(x, 10, 60, 30).collidepoint(event.pos):
                            draw_mode = mode
            else:
                drawing = True
                start_pos = (mx, my)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos and mouse_y >= 50:
                end_pos = (mx, my)
                x1, y1 = start_pos
                x2, y2 = end_pos

                if draw_mode == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                elif draw_mode == 'rect':
                    rect = pygame.Rect(start_pos, (x2 - x1, y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, brush_size)

                elif draw_mode == 'circle':
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    radius = int(math.hypot(x2 - x1, y2 - y1) / 2)
                    pygame.draw.circle(canvas, current_color, center, radius, brush_size)

                elif draw_mode == 'square':
                    size = min(abs(x2 - x1), abs(y2 - y1))
                    rect = pygame.Rect(x1, y1, size if x2 > x1 else -size, size if y2 > y1 else -size)
                    pygame.draw.rect(canvas, current_color, rect, brush_size)

                elif draw_mode == 'right_triangle':
                    points = [start_pos, (x2, y2), (x1, y2)]
                    pygame.draw.polygon(canvas, current_color, points, brush_size)

                elif draw_mode == 'equilateral_triangle':
                    side = int(math.hypot(x2 - x1, y2 - y1))
                    height = int((math.sqrt(3) / 2) * side)
                    points = [
                        (x1, y1),
                        (x1 - side // 2, y1 + height),
                        (x1 + side // 2, y1 + height)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, brush_size)

                elif draw_mode == 'rhombus':
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                    pygame.draw.polygon(canvas, current_color, points, brush_size)

                drawing = False

    # Eraser (active while mouse held)
    if drawing and draw_mode == 'eraser' and mouse_y >= 50:
        pygame.draw.circle(canvas, ERASER_COLOR, (mx, my), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()