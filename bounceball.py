import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 10
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)  # Light blue color for the level indicator

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")
font = pygame.font.Font(None, 36)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Initialize variables for the game
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]  # Faster starting speed
platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
platform_speed = 10
score = 0
lives = 3
current_level = 1
platform_color = ORANGE  # Initialize platform color
# Load the background image for the current level
start_background = pygame.image.load("start-background.jpg")
victory_background = pygame.image.load("start-background.jpg")
game_over_background = pygame.image.load("start-background.jpg")
spiel_background = pygame.image.load("spiel-background.jpg")

# Load the ball image
ball_image = pygame.image.load('melone.png')
ball_rect = ball_image.get_rect()
ball_rect.center = ball_pos

# Load the platform image
platform_image = pygame.image.load('sofa.png')
platform_rect = platform_image.get_rect()
platform_rect.topleft = platform_pos

# Functions for screens
def start_screen():
    screen.blit(start_background, (0, 0))
    show_text_on_screen("Bouncing Ball Game", 50, HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 30, HEIGHT // 3)
    show_text_on_screen("Move the platform with arrow keys...", 30, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

def game_over_screen():
    screen.blit(game_over_background, (0, 0))
    show_text_on_screen("Game Over", 50, HEIGHT // 3)
    show_text_on_screen(f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def victory_screen():
    screen.blit(victory_background, (0, 0))
    show_text_on_screen("Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(f"You've won with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
def show_text_on_screen(text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)
# Main game loop
start_screen()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    # Move the platform
    platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    platform_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platform_speed

    # Ensure the platform stays within the screen boundaries
    platform_pos[0] = max(0, min(platform_pos[0], WIDTH - PLATFORM_WIDTH))
    platform_pos[1] = max(0, min(platform_pos[1], HEIGHT - PLATFORM_HEIGHT))
    platform_rect.topleft = platform_pos

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]
    ball_rect.center = ball_pos  # Update the ball image position

    # Bounce off the walls
    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]

    if ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Check if the ball hits the platform
    if ball_rect.colliderect(platform_rect) and ball_speed[1] > 0:
        ball_speed[1] = -ball_speed[1]
        score += 1

    # Check if the ball falls off the screen
    if ball_pos[1] >= HEIGHT:
        # Decrease lives
        lives -= 1
        if lives == 0:
            game_over_screen()
            start_screen()  # Restart the game after game over
            score = 0
            lives = 3
            current_level = 1
        else:
            # Reset the ball position
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            # Randomize the ball speed
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]

    # Clear the screen
    screen.blit(spiel_background, (0, 0))

    # Draw the ball
    screen.blit(ball_image, ball_rect)

    # Draw the platform
    screen.blit(platform_image, platform_rect)

    # Display information
    info_line_y = 10  # Adjust the vertical position as needed
    info_spacing = 75  # Adjust the spacing as needed

    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top left (next to the score)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the lives in a red rectangle at the top left (next to the level)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, RED, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()