import pygame
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt
import os

# Initialize Pygame
try:
    pygame.init()
except pygame.error as e:
    print(f"Error initializing Pygame: {e}")
    sys.exit()

# Screen and grid settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GRID_SIZE = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (250, 156, 28)
YELLOW = (255, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat and Mouse Split-Screen Game")
clock = pygame.time.Clock()

# Fonts
try:
    font = pygame.font.Font("fonts/Manti Sans Bold Demo.otf", 62)
    # small_font = pygame.font.Font("fonts/Manti Sans Light Demo.otf", 20) 
    xsmall_font = pygame.font.Font("fonts/Manti Sans Light Demo.otf", 20)

except pygame.error as e:
    print(f"Error loading fonts: {e}")
    sys.exit()

# Load sounds
try:
    pygame.mixer.music.load("tracks/background_music_2.mp3")
    game_music = "tracks/background_music_1.mp3"
    enemy_defeat_sound = pygame.mixer.Sound("tracks/mouse_hit5.mp3")
    win_sound = pygame.mixer.Sound("tracks/win_sound.mp3")
    lose_sound = pygame.mixer.Sound("tracks/lose_sound.mp3")
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    sys.exit()

LOSE_DELAY = 500  # 0.5 seconds

# Play main menu music
pygame.mixer.music.play(-1)
# Define the file path for logs
LOG_FILE_PATH = "logs/game_logs.csv"
# Helper function to append non-empty rows to DataFrame and save to file
def append_log_data(dataframe, new_data):
    try:
        new_data_df = pd.DataFrame(new_data)
        # Exclude empty or all-NA rows explicitly before concatenating
        new_data_df = new_data_df.dropna(how='all')
        if not new_data_df.empty:
            dataframe = pd.concat([dataframe, new_data_df], ignore_index=True)
            # Save the updated dataframe to the log file
            dataframe.to_csv(LOG_FILE_PATH, index=False)  # Save as CSV file
        return dataframe
    except Exception as e:
        print(f"Error appending log data: {e}")
        return dataframe

def draw_grid(offset=0):
    """Draws the grid lines on the screen."""
    for x in range(offset, SCREEN_WIDTH // 2 + offset, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (offset, y), (SCREEN_WIDTH // 2 + offset, y))

def draw_wall():
    """Draws the dividing wall between the two halves of the screen."""
    pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 2, 0, 4, SCREEN_HEIGHT))

class Mouse:
    def __init__(self, offset=0, use_image=False):
        self.x = random.randint(0, SCREEN_WIDTH // GRID_SIZE // 2 - 1) * GRID_SIZE + offset
        self.y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        self.speed = 2
        self.health = 100
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.offset = offset
        self.use_image = use_image
        if self.use_image:
            try:
                # Load images for each direction
                self.images = {
                    "UP": pygame.image.load("images/mouse_up.png"),
                    "DOWN": pygame.image.load("images/mouse_down.png"),
                    "LEFT": pygame.image.load("images/mouse_left.png"),
                    "RIGHT": pygame.image.load("images/mouse_right.png")
                }
                # Scale images to grid size
                self.images = {key: pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE)) for key, img in self.images.items()}
                self.image = self.images[self.direction]
            except pygame.error as e:
                print(f"Error loading mouse images: {e}")
                self.use_image = False  # Fallback to default square if image loading fails

    def move(self):
        """Moves the mouse randomly within the grid."""
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
            if self.use_image:
                self.image = self.images[self.direction]  # Update the image based on the direction

        # Keep mouse within grid bounds
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
        """Draws the mouse and its health bar."""
        if self.use_image:
            screen.blit(self.image, (self.x, self.y))  # Draw the mouse image
        else:
            pygame.draw.rect(screen, GRAY, (self.x, self.y, GRID_SIZE, GRID_SIZE))  # Draw the gray box

        # Draw health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 5, GRID_SIZE * (self.health / 100), 5))

    def take_damage(self, damage):
        """Reduces the mouse's health."""
        self.health -= damage


class Mousetrap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = GRID_SIZE * 3  # Effective range of the trap
        self.damage = 5  # Incremental damage per attack
        self.cooldown = 40  # Time (in frames) between attacks
        self.timer = 0  # Timer to handle cooldowns

    def attack(self, mice):
        """Attacks mice within range incrementally."""
        if self.timer == 0:  # If trap is ready to attack
            for mouse in mice:
                # Calculate Euclidean distance to the mouse
                distance = ((self.x - mouse.x) ** 2 + (self.y - mouse.y) ** 2) ** 0.5
                if distance <= self.range:  # If mouse is in range
                    mouse.take_damage(self.damage)  # Apply incremental damage
                    pygame.mixer.Sound.play(enemy_defeat_sound)  # Play attack sound
                    self.timer = self.cooldown  # Reset cooldown timer
                    break  # Stop attacking other mice this frame

        # Decrease timer if not ready yet
        if self.timer > 0:
            self.timer -= 1

    def draw(self, offset=0):
        """Draws the mousetrap."""
        pygame.draw.circle(screen, ORANGE, (self.x + offset, self.y), GRID_SIZE // 2)


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = []

    def initialize_population(self):
        """Create initial random population of mousetraps."""
        for _ in range(self.population_size):
            mousetraps = [
                (random.randint(SCREEN_WIDTH // 2 // GRID_SIZE, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                 random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
                for _ in range(random.randint(5, 10))
            ]
            self.population.append(mousetraps)

    def fitness(self, mousetraps, mice):
        """Calculate fitness as the number of mice in range."""
        fitness = 0
        for trap_x, trap_y in mousetraps:
            for mouse in mice:
                distance = ((trap_x - mouse.x) ** 2 + (trap_y - mouse.y) ** 2) ** 0.5
                if distance <= GRID_SIZE * 3:  # Effective range
                    fitness += 1
        return fitness

    def select_parents(self, mice):
        """Select parents based on fitness."""
        fitness_scores = [self.fitness(mousetraps, mice) for mousetraps in self.population]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, self.population), reverse=True)]
        return sorted_population[:2]

    def crossover(self, parent1, parent2):
        """Perform crossover to create offspring."""
        split = len(parent1) // 2
        child = parent1[:split] + parent2[split:]
        return child

    def mutate(self, mousetraps):
        """Mutate some traps with random positions."""
        if random.random() < self.mutation_rate:
            index = random.randint(0, len(mousetraps) - 1)
            mousetraps[index] = (
                random.randint(SCREEN_WIDTH // 2 // GRID_SIZE, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
            )

    def create_new_generation(self, mice):
        """Generate a new population."""
        # Select the two best parents based on fitness
        parent1, parent2 = self.select_parents(mice)
        
        # Clear the current population
        self.population = []
        
        # Generate a new population
        for _ in range(self.population_size):
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            self.population.append(child)

def win(winner, n):
    pygame.mixer.music.stop()
    if winner == "AI":
        pygame.time.delay(LOSE_DELAY)
        pygame.mixer.Sound.play(lose_sound)
    else:
        pygame.time.delay(LOSE_DELAY)
        pygame.mixer.Sound.play(win_sound)

    font_large = pygame.font.Font("fonts/Manti Sans Bold Demo.otf", 72)
    font_small = pygame.font.Font("fonts/Manti Sans Black Demo.otf", 36)
    font_xsmall = pygame.font.Font("fonts/Manti Sans Light Demo.otf", 20)

    while True:
        screen.fill(BLACK)
        win_text = font_large.render(f"{winner} Wins!", True, WHITE)
        kills_text = font_small.render(f"Total Kills: {n}", True, WHITE)
        restart_text = font_xsmall.render("Press BACKSPACE for Main Menu", True, WHITE)
        restart_text2 = font_xsmall.render("Press S to show Performance Graph", True, WHITE)
        restart_text3 = font_xsmall.render("Press ESC to Quit", True, WHITE)

        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(kills_text, (SCREEN_WIDTH // 2 - kills_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(restart_text2, (SCREEN_WIDTH // 2 - restart_text2.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(restart_text3, (SCREEN_WIDTH // 2 - restart_text3.get_width() // 2, SCREEN_HEIGHT // 2 + 90))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    main_menu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    visualize_performance()
                    main_menu()


def visualize_performance():
    """Visualizes the logged performance data."""
    try:
        global log_data

        # Player's performance graph
        plt.figure(figsize=(10, 6))
        plt.plot(log_data['Player_Mousetraps'], log_data['Player_Kills'], label='Player Kills', color='blue')
        plt.xlabel('Number of Mousetraps Placed')
        plt.ylabel('Player Kills')
        plt.title('Player Performance')
        plt.grid()
        plt.legend()
        plt.show()

        # AI's performance graph
        plt.figure(figsize=(10, 6))
        plt.plot(log_data['Generation'], log_data['AI_Kills'], label='AI Kills', color='red')
        plt.plot(log_data['Generation'], log_data['Average_AI_Health'], label='Average AI Health', color='green')
        plt.xlabel('Generation')
        plt.ylabel('AI Metrics')
        plt.title('AI Performance')
        plt.grid()
        plt.legend()
        plt.show()

        # Comparative graph of Player's and AI's kills
        plt.figure(figsize=(10, 6))
        plt.plot(log_data['Player_Mousetraps'], log_data['Player_Kills'], label='Player Kills', color='blue')
        plt.plot(log_data['Generation'], log_data['AI_Kills'], label='AI Kills', color='red')
        plt.xlabel('Number of Mousetraps Placed (Player) / Generation (AI)')
        plt.ylabel('Number of Kills')
        plt.title('Player vs AI Kills Comparison')
        plt.grid()
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Error visualizing performance data: {e}")


# Main function and menu

# def main_menu():
#     while True:
#         screen.fill(BLACK)
#         title_text = font.render("Cat And Mouse Game", True, WHITE)
#         play_text = xsmall_font.render("Press ENTER to Play", True, WHITE)
#         quit_text = xsmall_font.render("Press ESC to Quit", True, WHITE)

#         screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
#         screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT // 2))
#         screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     main()
#                 if event.key == pygame.K_ESCAPE:

#                     pygame.quit()
#                     sys.exit()
#                 # if event.key == pygame.K_r:
#                 #     visualize_performance()

def main_menu():
    try:
        # Load background image
        background_image = pygame.image.load("images/background_image.png")
        background_image = pygame.transform.scale(background_image, (500, 500))
        background_image_position = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2 - 60)
        
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit()

    selected = 0
    menu_options = ["Start Game", "Quit Game"]

    while True:
        screen.blit(background_image, background_image_position)  # Blit the background image
        text = xsmall_font.render("Press ENTER to Play", True, WHITE)
        title = font.render("Cat and Mouse Game", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(menu_options):
            color = WHITE if i == selected else GRAY
            text = xsmall_font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    if menu_options[selected] == "Start Game":
                        main()
                    elif menu_options[selected] == "Quit Game":
                        pygame.quit()
                        sys.exit()


def main():
    pygame.mixer.music.load(game_music)

    pygame.mixer.music.play(-1)
    
    mousetraps_player = []
    player_mousetraps_count = 0
    n = 15
    mice = [Mouse(use_image=True) for _ in range(n)]  # Player's mice
    mice_ai = [Mouse(offset=SCREEN_WIDTH // 2, use_image=True) for _ in range(n)]  # AI's mice

    ga = GeneticAlgorithm(population_size=n, mutation_rate=0.1)
    ga.initialize_population()
    mousetraps_ai = ga.population[0]

    player_kills = 0
    ai_kills = 0
    global log_data
    log_data = pd.DataFrame(columns=['Generation', 'AI_Kills', 'Player_Kills', 'Average_AI_Health'])

    generation = 0
    f=5 #frequency of generating a new generation

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
                    mousetraps_player.append(Mousetrap(grid_x, grid_y))
                    player_mousetraps_count += 1

        for mouse in mice[:]:
            mouse.move()
            if mouse.health <= 0:
                mice.remove(mouse)
                player_kills += 1
                if player_kills == n:
                    win("Player", n)

        for mouse in mice_ai[:]:
            mouse.move()
            if mouse.health <= 0:
                mice_ai.remove(mouse)
                ai_kills += 1
                if ai_kills == n:
                    win("AI", n)
        
        # Genetic Algorithm update. Create a new generation every n frames
        
        if generation % f == 0:
            ga.create_new_generation(mice_ai)

        # UI update
        avg_health = sum(mouse.health for mouse in mice_ai) / len(mice_ai) if mice_ai else 0
        if generation % f == 0:
            log_data = append_log_data(log_data, {
            'Generation': [generation],
            'AI_Kills': [ai_kills],
            'Player_Kills': [player_kills],
            'Average_AI_Health': [avg_health],
            'Player_Mousetraps': [player_mousetraps_count]  # Log mousetrap count
            })

        generation += 1

        screen.fill(BLACK)
        draw_wall()

        for mousetrap in mousetraps_player:
            mousetrap.draw()
            mousetrap.attack(mice)

        for mousetrap_pos in ga.population[0]:
            mousetrap = Mousetrap(mousetrap_pos[0], mousetrap_pos[1])
            mousetrap.draw(offset=0)
            mousetrap.attack(mice_ai)

        for enemy in mice:
            enemy.draw()
        for enemy in mice_ai:
            enemy.draw()

        # Display Player and AI scores
        player_score_text = xsmall_font.render(f"Player's Score: {player_kills}", True, WHITE)
        ai_score_text = xsmall_font.render(f"AI's Score: {ai_kills}", True, WHITE)
        screen.blit(player_score_text, (10, 10))
        screen.blit(ai_score_text, (SCREEN_WIDTH // 2 + 10, 10))

        # Display mousetrap count and generation
        player_trap_text = xsmall_font.render(f"Player Mousetraps: {player_mousetraps_count}", True, WHITE)
        generation_text = xsmall_font.render(f"No. of Generations: {generation // f}", True, WHITE)

        screen.blit(player_trap_text, (10, 40))
        screen.blit(generation_text, (SCREEN_WIDTH // 2 + 10, 40))

        pygame.display.flip()
        clock.tick(FPS)
main_menu()
