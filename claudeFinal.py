import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen and grid settings
SCREEN_WIDTH = 1200  # Double the width for split screen
SCREEN_HEIGHT = 600
GRID_SIZE = 5  # Each grid cell is 40x40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (250, 156, 28)
YELLOW = (255, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(" Cat and Mouse Split-Screen Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)  # Small Font for Instructions

# Draw the grid
def draw_grid(offset=0):
    for x in range(offset, SCREEN_WIDTH // 2 + offset, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (offset, y), (SCREEN_WIDTH // 2 + offset, y))

def draw_wall():
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 2, 0, 4, SCREEN_HEIGHT))

# --- Load Music and Sound Effects ---
pygame.mixer.music.load("tracks/background_music_2.mp3")  # Main menu background music
game_music = "tracks/background_music_1.mp3"  # In-game background music
# tower_place_sound = pygame.mixer.Sound("tower_place.wav")  # Sound for placing a tower
enemy_defeat_sound = pygame.mixer.Sound("tracks/enemy_hit5.mp3")  # Sound for enemy defeat
win_sound = pygame.mixer.Sound("tracks/win_sound.mp3")  # Sound for player win
lose_sound = pygame.mixer.Sound("tracks/lose_sound.mp3")  # Sound for AI win

# Add a delay before playing the losing sound (in milliseconds)
LOSE_DELAY = 500  # 0.5 seconds

# Play main menu music
pygame.mixer.music.play(-1)  # Loop forever

# Enemy class
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

        # Randomly change direction
        if random.randint(0, 50) == 0:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        # Keep enemy within grid bounds
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
        pygame.draw.rect(screen, GRAY, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (self.x, self.y - 5, GRID_SIZE * (self.health / 100), 5))

    def take_damage(self, damage):
        self.health -= damage

# Tower class
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
                    enemy.take_damage(self.damage)
                    pygame.mixer.Sound.play(enemy_defeat_sound)
                    self.timer = self.cooldown
                    return True
        if self.timer > 0:
            self.timer -= 1
        return False

    def draw(self, offset=0):
        pygame.draw.circle(screen, ORANGE, (self.x + offset, self.y), GRID_SIZE // 2)

# Genetic Algorithm for AI tower placement
class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []

    def initialize_population(self):
        for _ in range(self.population_size):
            towers = [
                (random.randint(0, SCREEN_WIDTH // GRID_SIZE // 2 - 1) * GRID_SIZE + SCREEN_WIDTH // 2 + GRID_SIZE // 2,
                 random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE + GRID_SIZE // 2)
                for _ in range(random.randint(5, 10))
            ]
            self.population.append(towers)

def win(winner, n):
    pygame.mixer.music.stop()  # Stop game music

    if winner == "AI":  # Check if the AI wins
        pygame.time.delay(LOSE_DELAY)  # Add delay before playing lose sound
        pygame.mixer.Sound.play(lose_sound)  # Play lose sound
    else:
        pygame.mixer.Sound.play(win_sound)
    """
    Displays the winning message and waits for the player to quit or restart.
    :param winner: "Player" or "AI"
    :param n: Number of kills required to win
    """
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)
        # Display win text
        win_text = font_large.render(f"{winner} Wins!", True, WHITE)
        kills_text = font_small.render(f"Total Kills: {n}", True, WHITE)
        restart_text = font_small.render("Press ENTER to Restart or ESC to Quit", True, WHITE)

        # Center the text
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(kills_text, (SCREEN_WIDTH // 2 - kills_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart the game
                    main()
                if event.key == pygame.K_ESCAPE:  # Go to main menu
                    main_menu()

# Main game loop
def main():
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)  # Start game music
    towers_player = []
    n = 5  # Number of enemies
    enemies = [Enemy() for _ in range(n)]
    enemies_ai = [Enemy(offset=SCREEN_WIDTH // 2) for _ in range(n)]

    ga = GeneticAlgorithm(population_size=n, mutation_rate=0.1)
    ga.initialize_population()
    towers_ai = ga.population[0]

    player_kills = 0
    ai_kills = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < SCREEN_WIDTH // 2:
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
                    towers_player.append(Tower(grid_x, grid_y))

        # Update enemies and check player win condition
        for enemy in enemies[:]:
            enemy.move()
            if enemy.health <= 0:
                enemies.remove(enemy)
                player_kills += 1
                if player_kills == n:  # Player wins
                    win("Player", n)

        # Update AI enemies and check AI win condition
        for enemy in enemies_ai[:]:
            enemy.move()
            if enemy.health <= 0:
                enemies_ai.remove(enemy)
                ai_kills += 1
                if ai_kills == n:  # AI wins
                    win("AI", n)

        # Draw game elements
        screen.fill(BLACK)
        draw_wall()

        for tower in towers_player:
            tower.draw()
            tower.attack(enemies)

        for tower_pos in towers_ai:
            tower = Tower(tower_pos[0], tower_pos[1])
            tower.draw(offset=SCREEN_WIDTH // 2)
            tower.attack(enemies_ai)

        for enemy in enemies:
            enemy.draw()
        for enemy in enemies_ai:
            enemy.draw()

        # Display scores
        font_small = pygame.font.Font(None, 36)
        player_score_text = font_small.render(f"Player's Score: {player_kills}", True, WHITE)
        ai_score_text = font_small.render(f"AI's Score: {ai_kills}", True, WHITE)
        screen.blit(player_score_text, (10, 10))
        screen.blit(ai_score_text, (SCREEN_WIDTH // 2 + 10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# Main Menu
def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Cat And Mouse Game", True, WHITE)
        start_text = small_font.render("Press ENTER to Start", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()

if __name__ == "__main__":
    main_menu()
