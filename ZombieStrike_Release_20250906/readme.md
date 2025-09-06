# Operation: Zombie Strike

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.5.2-green.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tactical survival game where you must eliminate zombies and survive in a post-apocalyptic world. Built with Python and Pygame.

## Download and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. **Download the latest release** from the [Releases](https://github.com/yourusername/zombie-strike/releases) page
2. **Extract the ZIP file** to your preferred location
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Launch the game**:
   ```bash
   python Tatipamula_Culminating.py
   ```
   Or use the launcher:
   ```bash
   python launch_game.py
   ```

## Game Overview

Operation: Zombie Strike is a 2D side-scrolling shooter where players take on the role of a military operative tasked with clearing an area of zombies. The game features dynamic day/night cycles, multiple waves of enemies, and various weapons at your disposal.

## Features

### Core Gameplay
- Three challenging waves of zombies with increasing difficulty
- Dynamic day/night cycle affecting the game's atmosphere
- Multiple weapons: semi-automatic rifle and grenades
- Health and ammunition management system
- Wave-based progression system
- Mission completion with extraction cutscene

### Visual Elements
- Smooth character animations for player and zombies
- Dynamic background transitions between day and night
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
