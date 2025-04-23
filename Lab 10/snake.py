import pygame
import random
import sys
import time
import db

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Multi Fruit Version")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# === Database setup ===
db.create_tables()

walls = {
    2: [(10, y) for y in range(5, 15)],
    3: [(x, 10) for x in range(5, 20)],
    4: [(15, y) for y in range(3, 17)] + [(x, 5) for x in range(10, 20)]
}

def show_leaderboard():
    screen.fill(BLACK)
    leaders = db.get_top_scores()
    title = font.render("Leaderboard", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    for i, (name, score) in enumerate(leaders):
        text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 60 + i * 30))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False

def main_menu():
    while True:
        screen.fill(BLACK)
        title = font.render("Welcome to Snake Game", True, GREEN)
        play = font.render("1. New Game", True, WHITE)
        resume = font.render("2. Continue Last Game", True, WHITE)
        lead = font.render("3. Leaderboard", True, WHITE)
        quit_text = font.render("4. Quit", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        screen.blit(play, (WIDTH // 2 - play.get_width() // 2, 120))
        screen.blit(resume, (WIDTH // 2 - resume.get_width() // 2, 170))
        screen.blit(lead, (WIDTH // 2 - lead.get_width() // 2, 220))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 270))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'new'
                elif event.key == pygame.K_2:
                    return 'continue'
                elif event.key == pygame.K_3:
                    show_leaderboard()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

menu_choice = main_menu()
username = input("Enter your username: ")
user_id = db.get_or_create_user(username)
if menu_choice == 'new':
    level, score = 1, 0
else:
    level, score = db.get_user_progress(user_id)

paused = False

class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = RIGHT
        self.grow_by = 0

    def move(self):
        head = self.body[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT) or new_head in self.body:
            return False

        if level in walls and new_head in walls[level]:
            return False

        self.body.append(new_head)

        if self.grow_by > 0:
            self.grow_by -= 1
        else:
            self.body.pop(0)
        return True

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*[i * CELL_SIZE for i in segment], CELL_SIZE, CELL_SIZE))

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

snake = Snake()
food = Food(snake.body)
speed = 10 + level * 2

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            db.save_progress(user_id, level, score)
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
            elif event.key == pygame.K_p:
                paused = not paused
                db.save_progress(user_id, level, score)

    if paused:
        continue

    if not snake.move():
        db.save_progress(user_id, level, score)
        break

    if food.is_expired():
        food = Food(snake.body)

    if snake.body[-1] == food.position:
        score += food.weight
        snake.grow_by += food.weight
        food = Food(snake.body)

        if score % 6 == 0:
            level += 1
            speed += 2

    snake.draw(screen)
    food.draw(screen)

    if level in walls:
        for wall in walls[level]:
            pygame.draw.rect(screen, GRAY, (*[i * CELL_SIZE for i in wall], CELL_SIZE, CELL_SIZE))

    hud = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(hud, (10, 10))

    pygame.display.update()
    clock.tick(speed)

screen.fill(BLACK)
msg = font.render("Game Over! Press any key to exit", True, BLUE)
screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
pygame.display.update()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
            waiting = False

pygame.quit()
