import pygame 
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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

# Background image
background_image = pygame.image.load("images/background2.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background music
pygame.mixer.init()
pygame.mixer.music.load("tracks/background_music_1.mp3")
pygame.mixer.music.play(-1)

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Score variables
player_score = 0
ai_score = 0
tick_count = 0  # Game ticks for logging

# Dataframe to log scores
columns = ["Tick", "Player_Score", "AI_Score"]
score_data = pd.DataFrame(columns=columns)

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
        self.range = GRID_SIZE * 5
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
                    return True
        if self.timer > 0:
            self.timer -= 1
        return False

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), GRID_SIZE // 2)