import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

# Grid size
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Multi Fruit Version")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = RIGHT
        self.grow_by = 0

    def move(self):
        head = self.body[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Wall or self collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT) or new_head in self.body:
            return False  # Game over

        self.body.append(new_head)

        if self.grow_by > 0:
            self.grow_by -= 1  # Don't shrink if we still need to grow
        else:
            self.body.pop(0)  # Normal movement
        return True

    def change_direction(self, new_dir):
        # Prevent reversing direction
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*[i * CELL_SIZE for i in segment], CELL_SIZE, CELL_SIZE))

# Food class with types
class Food:
    FRUITS = {
        'apple': {'color': RED, 'weight': 1},
        'orange': {'color': ORANGE, 'weight': 2},
        'blueberry': {'color': BLUE, 'weight': 2},
        'pineapple': {'color': YELLOW, 'weight': 3}
    }

    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)
        self.kind = random.choice(list(Food.FRUITS.keys()))
        self.color = Food.FRUITS[self.kind]['color']
        self.weight = Food.FRUITS[self.kind]['weight']
        self.spawn_time = time.time()
        self.lifetime = random.randint(3, 5)

    def random_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (*[i * CELL_SIZE for i in self.position], CELL_SIZE, CELL_SIZE))

    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime

# Game variables
snake = Snake()
food = Food(snake.body)
score = 0
level = 1
speed = 10

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    # Snake movement
    if not snake.move():
        break  # Game over

    # If food expired, spawn new one
    if food.is_expired():
        food = Food(snake.body)

    # Collision with food
    if snake.body[-1] == food.position:
        score += food.weight
        snake.grow_by += food.weight
        food = Food(snake.body)

        # Level up every 6 points
        if score % 6 == 0:
            level += 1
            speed += 2

    # Draw game elements
    snake.draw(screen)
    food.draw(screen)

    # Draw HUD
    hud = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(hud, (10, 10))

    pygame.display.update()
    clock.tick(speed)

# Game over screen
screen.fill(BLACK)
msg = font.render("Game Over! Press any key to exit", True, BLUE)
screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
pygame.display.update()

# Wait for keypress
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
            waiting = False

pygame.quit()