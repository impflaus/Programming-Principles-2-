import pygame
import random
import sys

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
BLUE = (0, 0, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Lab 8")
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
        self.grow = False

    def move(self):
        head = self.body[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Check wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False  # Game over

        # Check self collision
        if new_head in self.body:
            return False

        self.body.append(new_head)
        if not self.grow:
            self.body.pop(0)
        else:
            self.grow = False
        return True

    def change_direction(self, new_dir):
        # Prevent reverse direction
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*[i * CELL_SIZE for i in segment], CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*[i * CELL_SIZE for i in self.position], CELL_SIZE, CELL_SIZE))

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

    if not snake.move():
        break  # Game over

    # Check food collision
    if snake.body[-1] == food.position:
        score += 1
        snake.grow = True
        food = Food(snake.body)

        # Level up every 4 points
        if score % 4 == 0:
            level += 1
            speed += 2

    # Draw everything
    snake.draw(screen)
    food.draw(screen)

    # Draw score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(speed)

# Game over screen
screen.fill(BLACK)
msg = font.render("Game Over! Press any key to exit", True, BLUE)
screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
pygame.display.update()

# Wait for key press to exit
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waiting = False
        elif event.type == pygame.QUIT:
            waiting = False
pygame.quit()
