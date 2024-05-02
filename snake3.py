import pygame
import random
import psycopg2

pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
CELL_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
DISAPPEAR_TIME = random.randint(1000, 2000)  # Random time between 1 and 2 seconds in milliseconds

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game variables
snake = [(10, 10)]
snake_direction = RIGHT
food = (5, 5)
food_size = random.randint(1, 3) * CELL_SIZE  # Random size between 1 and 3 times the cell size
food_timer = pygame.time.get_ticks() + DISAPPEAR_TIME  # Set the initial timer for food disappearance
score = 0
level = 1
speed = 1

# Game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Game clock
clock = pygame.time.Clock()

# Database initialization
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                       password="4232", port="5433")
cur=conn.cursor()
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS user_scores (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    level INTEGER,
                    score INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')
conn.commit()

# Functions
def create_user():
    cursor.execute('INSERT INTO users (username) VALUES (%s) ON CONFLICT (username) DO NOTHING', (username,))
    conn.commit()

def get_user_id(username):
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else None

def get_user_level(user_id):
    cursor.execute('SELECT level FROM user_scores WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    user_level = cursor.fetchone()
    return user_level[0] if user_level else None

def save_score(user_id, level, score):
    cursor.execute('INSERT INTO user_scores (user_id, level, score) VALUES (%s, %s, %s)', (user_id, level, score))
    conn.commit()

def draw_snake():
    for segment in snake:
        pygame.draw.rect(window, SNAKE_COLOR, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(window, FOOD_COLOR, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, food_size, food_size))

def check_collision():
    if snake[0][0] < 0 or snake[0][0] >= WINDOW_WIDTH / CELL_SIZE or snake[0][1] < 0 or snake[0][1] >= WINDOW_HEIGHT / CELL_SIZE:
        return True
    if snake[0] in snake[1:]:
        return True
    return False

def generate_food():
    while True:
        x = random.randint(0, int(WINDOW_WIDTH / CELL_SIZE) - 1)
        y = random.randint(0, int(WINDOW_HEIGHT / CELL_SIZE) - 1)
        if (x, y) not in snake:
            return (x, y)

# Main game loop
running = True
paused = False
username = input("Enter your username: ")
create_user()
user_id = get_user_id(username)
user_level = get_user_level(user_id)
if user_level:
    print(f"Welcome back, {username}! Your current level is {user_level}.")
else:
    print(f"Welcome, {username}!")

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT
            elif event.key == pygame.K_p:
                paused = not paused  # Toggle pause
            elif event.key == pygame.K_s:
                save_score(user_id, level, score)  # Save the score

    if not paused:
        # Move the snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake = [new_head] + snake[:-1]

        # Check for collisions
        if check_collision():
            running = False

        # Check if the snake eats food
        if snake[0] == food:
            snake.append(snake[-1])  # Grow the snake
            score += 1
            if score % 3 == 0:
                level += 1
                speed += 2

            save_score(user_id, level, score)

            food = generate_food()
            food_size = random.randint(1, 3) * CELL_SIZE  # Random size between 1 and 3 times the cell size
            food_timer = pygame.time.get_ticks() + DISAPPEAR_TIME  # Reset the timer for food disappearance

        # Draw everything
        window.fill(BACKGROUND_COLOR)
        draw_snake()
        draw_food()

        # Display score and level
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        window.blit(level_text, (10, 40))

        pygame.display.update()

        # Control game speed
        clock.tick(speed)
    else:
        # Display pause message
        font = pygame.font.SysFont(None, 50)
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        window.blit(pause_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 25))
        pygame.display.update()

pygame.quit()