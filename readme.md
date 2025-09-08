# Zombie Strike

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.5.2-green.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intense 2D side-scrolling shooter where you must survive against waves of zombies in a post-apocalyptic world. Built with Python and Pygame.

## 🚀 Quick Start

### Prerequisites
- Windows OS
- No installation required - just download and play!

### How to Play
1. Download the latest `ZombieStrike.exe` from the [Releases](https://github.com/Tabulater/Zombie-Strike/releases) page
2. Double-click `ZombieStrike.exe` to start the game
3. Use the following controls:
   - **WASD** or **Arrow Keys**: Move
   - **Mouse**: Aim
   - **Left Click**: Shoot
   - **Right Click**: Throw grenade
   - **R**: Reload
   - **1-2**: Switch weapons
   - **ESC**: Pause game

## 🎮 Game Features

### Intense Combat
- Face relentless waves of zombies with increasing difficulty
- Dual-wield powerful weapons: assault rifle and grenades
- Strategic ammo and health management
- Challenging boss battles

### Immersive Experience
- Dynamic day/night cycle system
- High-quality sound effects and background music
- Smooth animations and visual effects
- Engaging mission progression

## 🛠 Development

### For Developers
If you want to modify the game, you'll need:
- Python 3.8+
- Pygame 2.5.2
- Other dependencies in `requirements.txt`

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python ZombieStrike.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- Game developed by [Your Name]
- Sound effects and music by [Credits]
- Special thanks to all playtesters
- Particle effects for explosions and projectiles
- Health bars and ammunition counters
- Wave information display
- Time display showing in-game time

### Audio
- Background music that changes based on game state
- Sound effects for:
  - Gunshots
  - Grenade explosions
  - Menu interactions

### User Interface
- Main menu with options for:
  - Starting the game
  - Viewing instructions
  - About section
  - Quitting
- Pause menu
- Wave completion screen
- Game over screen with statistics
- Mission briefing cutscene
- Extraction cutscene

## Controls

### Movement
- A/D or Left/Right Arrow Keys: Move left/right
- W or Up Arrow: Jump
- Left Shift: Sprint

### Combat
- Space: Shoot
- R: Reload
- Left Mouse Button: Throw grenade (hold to aim)

### Menu Navigation
- W/S or Up/Down Arrow Keys: Navigate options
- Enter: Select option
- ESC: Pause game/Return to menu

## Game Mechanics

### Player
- Health system with visual health bar
- Limited ammunition requiring strategic reloading
- Grenade system with trajectory preview
- Movement affected by gravity and jumping mechanics

### Zombies
- Three waves with increasing difficulty
- Each wave features:
  - More zombies
  - Increased zombie health
  - Faster movement speed
- Zombies can detect and chase the player
- Attack system with damage cooldown

### Environment
- Dynamic day/night cycle affecting visibility
- Ground collision system
- Screen scrolling based on player movement

### Weapons
1. Primary Weapon (Rifle)
   - Semi-automatic firing
   - Limited ammunition
   - Reload system
   - Bullet physics

2. Secondary Weapon (Grenades)
   - Limited supply
   - Trajectory preview
   - Area of effect damage
   - Explosion physics

## Technical Details

### Built With
- Python 3.x
- Pygame
- Visual Studio Code

### File Structure
- Main game file: `Culminating.py`
- Assets folder containing:
  - Character sprites
  - Background images
  - Sound effects
  - Music files

### Game States
1. Main Menu
2. Instructions
3. About Screen
4. Intro Cutscene
5. Gameplay
6. Wave Complete Screen
7. Game Over Screen
8. Extraction Cutscene

## Development

Created by: Aashrith Raj Tatipamula
For: Mrs. Ellacott's ICS3U Class
Version: 1.0.0

## Installation

1. Ensure Python 3.x is installed
2. Install required packages:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python Culminating.py
   ```

## Game Flow

1. Start at main menu
2. View mission briefing
3. Complete three waves of zombies
4. Survive until extraction
5. View mission statistics
6. Return to main menu

## Tips for Success

- Keep moving to avoid zombie attacks
- Use grenades strategically for groups of zombies
- Monitor your health and ammunition
- Time your jumps and attacks carefully
- Use the sprint feature to quickly reposition
- Aim grenades carefully using the trajectory preview
- Reload when safe, not during combat
- Watch the day/night cycle for optimal visibility
