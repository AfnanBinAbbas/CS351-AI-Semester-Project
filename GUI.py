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

