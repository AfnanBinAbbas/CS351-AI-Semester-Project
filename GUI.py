import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Split-Screen Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Enemy Class
class Enemy:
    def __init__(self, offset=0):
        self.x = random.randint(0, SCREEN_WIDTH // GRID_SIZE // 2 - 1) * GRID_SIZE + offset
        self.y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        self.speed = 2
        self.health = 100
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.offset = offset

    def move(self):
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed

        if random.randint(0, 50) == 0:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        if self.x < self.offset:
            self.x = self.offset
            self.direction = "RIGHT"
        elif self.x >= self.offset + (SCREEN_WIDTH // 2) - GRID_SIZE:
            self.x = self.offset + (SCREEN_WIDTH // 2) - GRID_SIZE
            self.direction = "LEFT"

        if self.y < 0:
            self.y = 0
            self.direction = "DOWN"
        elif self.y >= SCREEN_HEIGHT - GRID_SIZE:
            self.y = SCREEN_HEIGHT - GRID_SIZE
            self.direction = "UP"

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 5, GRID_SIZE * (self.health / 100), 5))

# Tower Class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = GRID_SIZE * 3
        self.damage = 20
        self.cooldown = 30
        self.timer = 0

    def attack(self, enemies):
        if self.timer == 0:
            for enemy in enemies:
                distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
                if distance <= self.range:
                    enemy.health -= self.damage
                    self.timer = self.cooldown
                    return
        if self.timer > 0:
            self.timer -= 1

    def draw(self, offset=0):
        pygame.draw.circle(screen, BLUE, (self.x + offset, self.y), GRID_SIZE // 2)

# Draw the grid
def draw_grid(offset=0):
    for x in range(offset, SCREEN_WIDTH // 2 + offset, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (offset, y), (SCREEN_WIDTH // 2 + offset, y))

def draw_wall():
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 2, 0, 4, SCREEN_HEIGHT))


# Background image
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background music
pygame.mixer.init()
pygame.mixer.music.load("tracks/background_music_1.mp3")
pygame.mixer.music.play(-1)

# Main game function
def main_game():
    enemies = [Enemy() for _ in range(10)]
    enemies_ai = [Enemy(offset=SCREEN_WIDTH // 2) for _ in range(10)]
    towers = []
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < SCREEN_WIDTH // 2:
                    towers.append(Tower(mouse_x, mouse_y))

        if not paused:
            # Draw background, grid, and wall
            screen.blit(background_image, (0, 0))
            draw_grid()
            draw_grid(offset=SCREEN_WIDTH // 2)
            draw_wall()

            # Update and draw enemies
            for enemy in enemies[:]:
                enemy.move()
                if enemy.health <= 0:
                    enemies.remove(enemy)
                enemy.draw()

            for enemy in enemies_ai[:]:
                enemy.move()
                if enemy.health <= 0:
                    enemies_ai.remove(enemy)
                enemy.draw()

            # Draw and update towers
            for tower in towers:
                tower.draw()
                tower.attack(enemies)

            # Update the display
            pygame.display.flip()
            clock.tick(FPS)

# Run main menu
if __name__ == "__main__":
    main_menu()
