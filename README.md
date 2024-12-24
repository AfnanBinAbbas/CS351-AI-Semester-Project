---

# Cat and Mouse Split-Screen Game 🎮

A split-screen **Cat and Mouse game** built using Python's Pygame library. The game allows players to place mousetraps strategically to eliminate enemies (mice) while competing against an AI using a **genetic algorithm** for mousetrap placement.
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## Features

-  **Split-Screen Gameplay**: Compete against the AI in a split-screen environment.
-  **Genetic Algorithm**: The AI uses a genetic algorithm to decide optimal mousetrap placement.
-  **Mousetrap Defense Mechanics**: Place mousetraps manually to attack and defeat incoming enemies (mice).
-  **Sound Effects and Music**: Background music and effects enhance gameplay.
-  **Dynamic Win Conditions**: Compete to eliminate a set number of enemies (mice) before the AI does.

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## How to Play

1. **Start the Game**:
   - Run the Python script.
   - Press `ENTER` at the main menu to begin.

2. **Placing Mousetraps**:
   - Use the **mouse** to click on the left side of the screen (Player's side) to place mousetraps.
   - Mousetraps will automatically attack nearby enemies (mice).

3. **Objective**:
   - Eliminate **5 enemies (mice)** before the AI to win the game.

4. **AI Side**:
   - The AI will automatically place mousetraps and eliminate enemies (mice) using its pre-calculated strategy.

5. **Winning**:
   - If you defeat all enemies (mice) first, you win.
   - If the AI eliminates all enemies (mice) first, the AI wins.

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## Controls

- **Mouse Click**: Place mousetraps on the player's grid.
- **ESC**: Quit the game at any time.
- **ENTER**: Start or restart the game.

---

## Dependencies

- **Python 3.x**
- **Pygame** (install via pip)

### Installation

1. Install Python and Pygame:
   ```bash
   pip install pygame

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## Directory Structure

2. Place all required files (e.g., sound and music files) in a folder structure as follows:

   ```
   Cat-and-Mouse-Game-using-Genetic-Algorithm-/
   ├── app.py     # The main game script
   ├── tracks/
   │     ├── background_music_1.mp3
   │     ├──background_music_2.mp3
   │     ├──background_music_3.mp3
   │     ├──game_over.mp3 
   │     ├──lose_sound.mp3
   │     ├──mouse_hit5.mp3
   │     ├──win_sound.mp3
   │     └──...
   ├── images/
   │     ├── mouse_up.png
   │     ├── mouse_down.png
   │     ├── mouse_right.png
   │     ├── mouse_left.png
   │     ├── mouse_image.png
   │     └──... 
   ├── fonts/
   │     ├── Manti Sans Black Demo.otf 
   │     ├── Manti Sans Bold Demo.otf 
   │     ├── Manti Sans Fixed Demo.otf
   │     ├── Manti Sans Light Demo.otf 
   │     ├── Manti Sans Regular Demo.otf
   │     └──... 
   ├── logs/
   │     ├── game_logs.csv
   │     └──...
   │   
   │ 
   ```

3. Run the game:
   ```bash
   python app.py
   ```

---

## Game Overview

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

### Grid Layout:
- The screen is divided into **two halves**:
   - Left Half: Player's area for mousetrap placement.
   - Right Half: AI's area for automated mousetrap placement.

### mousetraps:
- **Player**: Manually places mousetraps using mouse clicks.
- **AI**: Automatically places mousetraps using Genetic algorithm.

### enemies (mouse):
- Move randomly but stay within grid boundaries.
- Have health bars that decrease when hit by mousetraps.

---

## Notes

- Ensure all **music and sound effect files** are located in the specified `tracks` folder.
- Modify the `n` variable in the code to adjust the number of targets(mouse) required to win.

---

## Future Improvements (To-Do)

- Add more **enemy types** with different behaviors.
- Implement **upgradable mousetraps**.
- Introduce more **levels** and increasing difficulty.
- Improve AI mousetrap placement strategies for better competition.

---

## Credits

- **Game Development**: Built using Python and Pygame.

---

## License

This project is released under the **MIT License**. Feel free to modify and distribute it.

--- 

Enjoy the game!!
