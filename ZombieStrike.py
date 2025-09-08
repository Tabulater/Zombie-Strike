#Zombie Strike
#made by Aashrith Raj Tatipamula
#May 28th, 2025
#ICS3U
#-----------------------------
import pygame
import os
import math
import sys
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

# Initialize pygame and mixer for game and sound
pygame.init()
pygame.mixer.init()

# Game constants and configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
BACKGROUND_COLOR = (0, 100, 255)
GROUND_HEIGHT = 150
SCALE = 3
BULLET_SCALE = 0.01
GRAVITY = 1
JUMP_STRENGTH = -15
FRAME_DELAY = 150
BULLET_SPEED = 25
SHOOT_COOLDOWN = 300
SHOOT_FRAME_DELAY = 75
SHOOT_ANIMATION_DURATION = 300
BULLET_GRAVITY = 0
GRENADE_GRAVITY = 0.5
MAX_PULL_DISTANCE = 200
MIN_PULL_DISTANCE = 50
PULL_MULTIPLIER = 0.15
POWER_BAR_WIDTH = 200
POWER_BAR_HEIGHT = 20
POWER_BAR_PADDING = 10
AIM_LINE_COLOR = (255, 255, 255, 128)
AIM_LINE_WIDTH = 3
TRAJECTORY_DOTS = 20
TRAJECTORY_DOT_RADIUS = 2
BULLET_SPAWN_OFFSET = 25
EXPLOSION_RADIUS = 200
EXPLOSION_DURATION = 500
TIME_FONT_SIZE = 24
PLAYER_SPEED = 3
PLAYER_RUN_SPEED = 15
HOURS_PER_SECOND = 1 / 60
CAMO_GREEN = (0, 100, 0)
CAMO_BROWN = (139, 69, 19)
CAMO_TAN = (210, 180, 140)
MILITARY_RED = (220, 20, 60)
MILITARY_BLUE = (0, 0, 139)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 255, 0)
TEXT_COLOR = (240, 240, 240)
EXPLOSION_COLOR = (255, 165, 0)

# Create the main game window and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Strike")
clock = pygame.time.Clock()


class SoundManager:
    """Handles loading and playing sound effects and music."""
    def __init__(self):
        self.sounds = {}
        self.music = {}
        self.current_music = None
        self.volume = 0.5
        self.load_sounds()

    def load_sounds(self):
        # Load sound effects and music files
        self.sounds['gunshot'] = pygame.mixer.Sound(os.path.join("assets", "gunshot.mp3"))
        self.sounds['grenade'] = pygame.mixer.Sound(os.path.join("assets", "grenade.mp3"))
        self.music['menu'] = os.path.join("assets", "menu_music.mp3")
        self.music['wave'] = os.path.join("assets", "wave_music.mp3")
        for sound_name, sound in self.sounds.items():
            sound.set_volume(5.0 if sound_name == 'grenade' else self.volume)

    def play_sound(self, sound_name: str):
        # Play a sound effect by name
        if sound_name in self.sounds:
            if sound_name == 'grenade':
                self.sounds[sound_name].stop()
                self.sounds[sound_name].play()
                pygame.time.delay(50)
                self.sounds[sound_name].play()
            else:
                self.sounds[sound_name].play()

    def play_music(self, music_name: str, loops: int = -1):
        # Play background music by name
        if music_name in self.music and self.current_music != music_name:
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops)
            self.current_music = music_name

    def stop_music(self):
        # Stop any playing music
        pygame.mixer.music.stop()
        self.current_music = None

    def set_volume(self, volume: float):
        # Set the volume for all sounds and music
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.volume)


class HomePage:
    """Main menu and home screen for the game."""
    def __init__(self, screen, clock):
        self.screen, self.clock = screen, clock
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_option = 0
        self.options = ["Start Game", "About", "Quit"]
        self.showing_instructions = False
        self.instructions_scroll = 0
        self.max_scroll = 0
        self.title_alpha = 0
        self.title_scale = 0.8
        self.title_rotation = 0
        self.option_alpha = 0
        self.option_scale = 0.9
        self.animation_speed = 0.02
        self.particle_system = []
        self.mouse_pos = (0, 0)
        self.hover_effect = 0
        self.instructions_button_hovered = False
        self.military_font = pygame.font.Font(None, 72)
        self.background_image = pygame.image.load("Assets/Background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.init_particle_system()
        self.sound_manager = SoundManager()
        self.sound_manager.play_music('menu')
        self.settings_screen = None
        self.about_screen = None

    def init_particle_system(self):
        # Initialize background particles for menu effect
        for _ in range(50):
            self.particle_system.append({
                'pos': (random.randint(0, self.screen_width), random.randint(0, self.screen_height)),
                'velocity': (random.uniform(-1, 1), random.uniform(-1, 1)),
                'size': random.randint(2, 4),
                'alpha': random.randint(50, 150),
                'color': (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            })

    def update_particles(self):
        # Move and wrap menu background particles
        for p in self.particle_system:
            p['pos'] = (p['pos'][0] + p['velocity'][0], p['pos'][1] + p['velocity'][1])
            if p['pos'][0] < 0:
                p['pos'] = (self.screen_width, p['pos'][1])
            elif p['pos'][0] > self.screen_width:
                p['pos'] = (0, p['pos'][1])
            if p['pos'][1] < 0:
                p['pos'] = (p['pos'][0], self.screen_height)
            elif p['pos'][1] > self.screen_height:
                p['pos'] = (p['pos'][0], 0)

    def draw_particles(self):
        # Draw menu background particles
        for p in self.particle_system:
            s = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['color'], p['alpha']), (p['size'] / 2, p['size'] / 2), p['size'] / 2)
            self.screen.blit(s, p['pos'])

    def draw_overlay(self, alpha=100):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (0, 0))

    def create_gradient_surface(self, width, height, alpha_start=180, alpha_end=0):
        # Create a vertical gradient surface for UI boxes
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(height):
            alpha = int(alpha_start * (1 - y / height) + alpha_end * (y / height))
            pygame.draw.line(s, (0, 0, 0, alpha), (0, y), (width, y))
        return s

    def draw_box_with_effects(self, width, height, x, y, border_color=(255, 255, 255)):
        # Draw a UI box with gradient and border effects
        box_surface = self.create_gradient_surface(width, height)
        for i in range(3):
            alpha = 100 - i * 30
            pygame.draw.rect(box_surface, (*border_color, alpha), (i, i, width - i * 2, height - i * 2), 2)
        inner_border = 10
        pygame.draw.rect(box_surface, (200, 200, 200, 150), (inner_border, inner_border, width - 2 * inner_border, height - 2 * inner_border), 2)
        self.screen.blit(box_surface, (x, y))
        return box_surface

    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None, center=True, scale=1.0, rotation=0):
        # Draw text with shadow and optional scaling/rotation
        if font is None:
            font = self.font
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        if scale != 1.0 or rotation != 0:
            text_surface = pygame.transform.rotozoom(text_surface, rotation, scale)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_instructions_button(self):
        button_width = button_height = 40
        button_x = self.screen_width - button_width - 20
        button_y = 20
        button_surface = self.create_gradient_surface(button_width, button_height, 200, 100)
        for i in range(2):
            alpha = 150 - i * 50
            pygame.draw.rect(button_surface, (255, 255, 255, alpha), (i, i, button_width - i * 2, button_height - i * 2), 2)
        question_mark = "?"
        font_size = 32
        question_font = pygame.font.Font(None, font_size)
        shadow_surface = question_font.render(question_mark, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(button_width // 2 + 1, button_height // 2 + 1))
        button_surface.blit(shadow_surface, shadow_rect)
        text_color = (255, 215, 0) if self.instructions_button_hovered else (200, 200, 200)
        text_surface = question_font.render(question_mark, True, text_color)
        text_rect = text_surface.get_rect(center=(button_width // 2, button_height // 2))
        button_surface.blit(text_surface, text_rect)
        self.screen.blit(button_surface, (button_x, button_y))
        return pygame.Rect(button_x, button_y, button_width, button_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.showing_instructions:
                        self.showing_instructions = False
                        self.instructions_scroll = 0
                        return "menu"
                    return "quit"
                if not self.showing_instructions:
                    if event.key == pygame.K_w:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    if event.key == pygame.K_s:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    if event.key == pygame.K_RETURN:
                        selected = self.options[self.selected_option]
                        if selected == "Quit":
                            return "quit"
                        elif selected == "Start Game":
                            return "start_game"
                        elif selected == "About":
                            if not self.about_screen:
                                self.about_screen = AboutScreen(self.screen, self.clock)
                            action = self.about_screen.run()
                            if action == "menu":
                                self.about_screen = None
                            return action
            elif event.type == pygame.MOUSEWHEEL and self.showing_instructions:
                self.instructions_scroll = max(0, min(self.instructions_scroll - event.y * 30, self.max_scroll))
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                instructions_button_rect = pygame.Rect(self.screen_width - 60, 20, 40, 40)
                self.instructions_button_hovered = instructions_button_rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    instructions_button_rect = pygame.Rect(self.screen_width - 60, 20, 40, 40)
                    if instructions_button_rect.collidepoint(event.pos):
                        self.showing_instructions = True
                        self.instructions_scroll = 0
        return "menu"

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_overlay(100)
        self.update_particles()
        self.draw_particles()
        self.draw_instructions_button()
        box_width, box_height = 800, 250
        box_x = self.screen_width // 2 - box_width // 2
        box_y = self.screen_height // 4 - 100
        self.draw_box_with_effects(box_width, box_height, box_x, box_y)
        self.draw_text("OPERATION: ZOMBIE STRIKE", self.screen_width // 2, self.screen_height // 4, (255, 215, 0), self.military_font)
        self.draw_text("TACTICAL SURVIVAL", self.screen_width // 2, self.screen_height // 4 + 60, (107, 142, 35), self.military_font)
        for i, option in enumerate(self.options):
            y = self.screen_height // 2 + i * 50
            if i == self.selected_option:
                hover_scale = 1.1 + 0.05 * math.sin(pygame.time.get_ticks() * 0.005)
                self.draw_text(option, self.screen_width // 2, y, (255, 215, 0), scale=hover_scale)
                indicator_x = self.screen_width // 2 - 150
                pygame.draw.polygon(self.screen, (255, 215, 0), [(indicator_x, y), (indicator_x + 20, y - 10), (indicator_x + 20, y + 10)])
            else:
                self.draw_text(option, self.screen_width // 2, y, (200, 200, 200))
        controls = ["W/S to Navigate", "ENTER to Select", "ESC to Quit"]
        for i, control in enumerate(controls):
            self.draw_text(control, self.screen_width // 2, self.screen_height * 3 // 4 + i * 30, (200, 200, 200), self.small_font)
        self.draw_text("v1.0.0", self.screen_width - 50, self.screen_height - 20, (150, 150, 150), self.small_font)

    def draw_instructions(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_overlay(150)
        self.draw_text("HELP", self.screen_width // 2, 30, HIGHLIGHT, self.title_font)
        box_width, box_height = 800, 500
        box_x = self.screen_width // 2 - box_width // 2
        box_y = 100
        self.draw_box_with_effects(box_width, box_height, box_x, box_y)
        description = [
            "Welcome to Operation: Zombie Strike!",
            "A tactical survival game where you must eliminate zombies",
            "and survive in a post-apocalyptic world.",
            "",
            "CONTROLS:",
            "• Arrow Keys: Move left/right",
            "• Up Arrow: Jump",
            "• Left Shift: Sprint",
            "• Space: Shoot",
            "• R: Reload",
            "• Left Mouse Button: Throw grenade (hold to aim)",
            "• ESC: Pause game",
            "",
            "OBJECTIVES:",
            "• Eliminate all zombies in the area",
            "• Survive and maintain your health",
            "• Use your weapons strategically",
            "",
            "WEAPONS:",
            "• Primary Weapon: Semi-automatic rifle",
            "• Secondary Weapon: Grenades",
            "• Limited ammo - reload when needed",
            "",
            "TIPS:",
            "• Keep moving to avoid zombie attacks",
            "• Use grenades for groups of zombies",
            "• Monitor your health and ammo",
            "• Time your jumps and attacks carefully"
        ]
        content_height = len(description) * 25
        content_surface = pygame.Surface((box_width - 40, content_height), pygame.SRCALPHA)
        y = 0
        for line in description:
            if line.startswith("•"):
                text_surface = self.small_font.render(line, True, (200, 200, 200))
                content_surface.blit(text_surface, (30, y))
            else:
                text_surface = self.small_font.render(line, True, WHITE)
                content_surface.blit(text_surface, (20, y))
            y += 25
        self.max_scroll = max(0, content_height - box_height + 40)
        self.instructions_scroll = max(0, min(self.instructions_scroll, self.max_scroll))
        self.screen.blit(content_surface, (box_x + 20, box_y + 20), (0, self.instructions_scroll, box_width - 40, box_height - 40))
        if content_height > box_height - 40:
            scroll_bar_width = 10
            scroll_bar_height = (box_height - 40) * (box_height - 40) / content_height
            scroll_bar_y = box_y + 20 + (self.instructions_scroll / self.max_scroll) * (box_height - 40 - scroll_bar_height)
            pygame.draw.rect(self.screen, (50, 50, 50), (box_x + box_width - 30, box_y + 20, scroll_bar_width, box_height - 40))
            for y in range(int(scroll_bar_height)):
                alpha = int(200 * (1 - y / scroll_bar_height))
                pygame.draw.line(self.screen, (200, 200, 200, alpha), (box_x + box_width - 30, scroll_bar_y + y), (box_x + box_width - 20, scroll_bar_y + y))
        self.draw_text("Press ESC to return to menu", self.screen_width // 2, self.screen_height - 30, HIGHLIGHT)

    def run(self):
        while True:
            action = self.handle_events()
            if action != "menu":
                return action
            if self.showing_instructions:
                self.draw_instructions()
            else:
                self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)


class GameAssets:
    def __init__(self):
        self.actions = self._load_actions()
        self.day_bg = self._load_background("Day.jpg")
        self.night_bg = self._load_background("Night.jpg")
        self.font = pygame.font.Font(None, TIME_FONT_SIZE)
        self.bullet = self._load_bullet()
        self.recharge_frames = self._load_frames("Recharge", 13)
        self.throw_frames = self._load_frames("Throw", 9)
        self.zombie_frames = self._load_frames("Enemy/Run")
        self.zombie_attack_frames = self._load_frames("Enemy/Attack")

    def _load_frames(self, folder: str, frame_count: Optional[int] = None) -> List[pygame.Surface]:
        frames = []
        path = f"Assets/{folder}"
        files = sorted(os.listdir(path)) if not frame_count else [f"{i}.png" for i in range(frame_count)]
        for filename in files:
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(path, filename))
                scaled_size = (int(img.get_width() * SCALE), int(img.get_height() * SCALE))
                frames.append(pygame.transform.scale(img, scaled_size))
        return frames

    def _load_actions(self) -> Dict[str, List[pygame.Surface]]:
        return {action: self._load_frames(action) for action in ["Idle", "Walk", "Run", "Shoot", "Throw"]}

    def _load_background(self, filename: str) -> pygame.Surface:
        img = pygame.image.load(os.path.join("assets", filename))
        return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def _load_bullet(self) -> pygame.Surface:
        img = pygame.image.load(os.path.join("assets", "Bullet.png"))
        new_size = (int(img.get_width() * BULLET_SCALE), int(img.get_height() * BULLET_SCALE))
        return pygame.transform.scale(img, new_size)


class AnimationManager:
    def __init__(self, assets: GameAssets):
        self.assets = assets
        self.current_animation = "Idle"
        self.frame = 0
        self.timer = 0
        self.direction = "right"
        self.shooting = False
        self.shoot_timer = 0
        self.shoot_frame_timer = 0
        self.reloading = False
        self.reload_frame = 0
        self.reload_timer = 0
        self.throwing = False
        self.throw_frame = 0
        self.throw_timer = 0
        self.throw_frame_delay = 50
        self.last_throw_time = 0
        self.throw_cooldown = 1000

    def update(self, current_time: int, keys: pygame.key.ScancodeWrapper) -> None:
        if self.shooting:
            if current_time - self.shoot_frame_timer >= SHOOT_FRAME_DELAY:
                self.shoot_frame_timer = current_time
                self.frame = (self.frame + 1) % 4
            if current_time - self.shoot_timer >= SHOOT_ANIMATION_DURATION:
                self.shooting = False
                self.current_animation = "Idle"
                self.frame = 0
        if self.reloading:
            if current_time - self.reload_timer >= self.throw_frame_delay:
                self.reload_timer = current_time
                self.reload_frame += 1
                if self.reload_frame >= len(self.assets.recharge_frames):
                    self.reloading = False
                    self.reload_frame = 0
        if self.throwing:
            if current_time - self.throw_timer >= self.throw_frame_delay:
                self.throw_timer = current_time
                self.throw_frame += 1
                if self.throw_frame >= len(self.assets.throw_frames):
                    self.throwing = False
                    self.throw_frame = 0
        if not any([self.shooting, self.reloading, self.throwing]):
            self.timer += clock.get_time()
            if self.timer > FRAME_DELAY:
                self.timer = 0
                self.frame = (self.frame + 1) % len(self.assets.actions[self.current_animation])

    def draw(self, screen, x: int, y: int) -> None:
        if self.reloading:
            frame = self.assets.recharge_frames[self.reload_frame]
        elif self.throwing:
            frame = self.assets.throw_frames[self.throw_frame]
        else:
            current_frames = self.assets.actions.get(self.current_animation, self.assets.actions["Idle"])
            frame = current_frames[self.frame] if current_frames and 0 <= self.frame < len(current_frames) else None
        if frame:
            frame = pygame.transform.flip(frame, self.direction == "left", False)
            screen.blit(frame, (x - frame.get_width() // 2, y))

    def start_shoot(self, current_time: int) -> None:
        if not any([self.shooting, self.reloading, self.throwing]):
            self.shooting = True
            self.current_animation = "Shoot"
            self.frame = 0
            self.shoot_timer = current_time
            self.shoot_frame_timer = current_time

    def start_reload(self) -> None:
        if not self.reloading and not self.throwing:
            self.reloading = True
            self.reload_frame = 0
            self.reload_timer = pygame.time.get_ticks()

    def start_throw(self, current_time: int) -> None:
        if not self.throwing and not self.reloading and current_time - self.last_throw_time >= self.throw_cooldown:
            self.throwing = True
            self.throw_frame = 0
            self.throw_timer = current_time
            self.last_throw_time = current_time

    def set_animation(self, animation: str) -> None:
        if not any([self.shooting, self.reloading, self.throwing]):
            self.current_animation = animation

    def set_direction(self, direction: str) -> None:
        self.direction = direction


class Player:
    """
    Represents the player character in the game.
    Handles player movement, combat, health, and weapon management.
    """

    def __init__(self, x: int, y: int, width: int, height: int, assets: GameAssets, sound_manager: SoundManager):
        # Initialize player position and dimensions
        self.rect = pygame.Rect(x, y, width, height)
        self.original_x = x  # Store initial x position for reset
        self.original_y = y  # Store initial y position for reset

        # Game assets and sound management
        self.assets = assets  # Game assets (sprites, animations)
        self.sound_manager = sound_manager  # Sound manager for effects

        # Animation and movement
        self.animation = AnimationManager(assets)  # Manages player animations
        self.direction = "right"  # Current facing direction

        # Weapon systems
        self.bullets = []  # List of active bullets
        self.grenades = []  # List of active grenades
        self.explosions = []  # List of active explosions
        self.current_bullets = self.max_bullets = 30  # Ammo count
        self.current_grenades = self.max_grenades = 6  # Grenade count

        # Combat timing
        self.last_shot_time = 0  # Last time player fired
        self.reload_complete_time = None  # When reload will complete

        # Grenade aiming system
        self.is_aiming_grenade = False  # Whether player is aiming grenade
        self.grenade_trajectory_points = []  # Points for trajectory preview

        # Movement and physics
        self.jumping = False  # Whether player is jumping
        self.velocity = 0  # Current vertical velocity
        self.max_health = 100  # Maximum health
        self.current_health = self.max_health  # Current health

        # UI elements
        self.health_bar_width = 200  # Width of health bar
        self.health_bar_height = 20  # Height of health bar
        self.health_bar_padding = 10  # Padding around health bar

        # Grenade aiming system
        self.grenade_aim_start_pos = (0, 0)  # Start position for grenade aim
        self.grenade_aim_current_pos = (0, 0)  # Current aim position
        self.grenade_power = 0  # Current grenade throw power

        # UI and timing
        self.font = pygame.font.Font(None, 36)  # Font for UI elements
        self.last_damage_time = 0  # Last time player took damage
        self.damage_cooldown = 1000  # Time between damage events

    def take_damage(self, amount: int) -> None:
        """
        Handles player taking damage with cooldown system.

        Args:
            amount (int): Amount of damage to take
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_cooldown:
            self.current_health = max(0, self.current_health - amount)
            self.last_damage_time = current_time

    def update_projectiles(self) -> None:
        """
        Updates all projectiles (bullets, grenades, explosions).
        Handles movement, collisions, and cleanup.
        """
        current_time = pygame.time.get_ticks()

        # Update bullets
        self.bullets = [bullet for bullet in self.bullets if not self._is_off_screen(bullet['rect'])]
        for bullet in self.bullets:
            bullet['rect'].x += bullet['velocity'][0]
            bullet['rect'].y += bullet['velocity'][1]

        # Update grenades
        for grenade in self.grenades[:]:
            grenade['rect'].x += grenade['velocity'][0]
            grenade['rect'].y += grenade['velocity'][1]

            # Handle grenade landing
            if grenade['rect'].bottom >= self.original_y + self.rect.height:
                grenade['rect'].bottom = self.original_y + self.rect.height
                grenade['velocity'] = (0, 0)

                if not grenade.get('exploded', False):
                    grenade['exploded'] = True
                    # Play explosion sound multiple times for extra impact
                    self.sound_manager.play_sound('grenade')
                    pygame.time.delay(100)  # Add delay to ensure sound plays
                    self.sound_manager.play_sound('grenade')
                    self.explosions.append({
                        'pos': (grenade['rect'].centerx, grenade['rect'].centery),
                        'start_time': current_time,
                        'radius': 0,
                        'max_radius': EXPLOSION_RADIUS,
                        'damage': 150
                    })
                    self.grenades.remove(grenade)
            else:
                grenade['velocity'] = (grenade['velocity'][0], grenade['velocity'][1] + GRENADE_GRAVITY)
                grenade['angle'] += grenade['rotation_speed']

            if self._is_off_screen(grenade['rect']):
                self.grenades.remove(grenade)

        # Update explosions
        self.explosions = [explosion for explosion in self.explosions
                          if current_time - explosion['start_time'] < EXPLOSION_DURATION]
        for explosion in self.explosions:
            progress = (current_time - explosion['start_time']) / EXPLOSION_DURATION
            explosion['radius'] = int(explosion['max_radius'] * progress)

        # Check reload completion
        if self.reload_complete_time and current_time >= self.reload_complete_time:
            self.current_bullets = self.max_bullets
            self.reload_complete_time = None

    def _is_off_screen(self, rect: pygame.Rect) -> bool:
        return (rect.right < 0 or rect.left > SCREEN_WIDTH or
                rect.bottom < 0 or rect.top > SCREEN_HEIGHT)

    def shoot(self, current_time: int, world_offset: int) -> None:
        if (current_time - self.last_shot_time >= SHOOT_COOLDOWN and
            not self.animation.shooting and
            not self.animation.reloading and
            self.current_bullets > 0):
            self.animation.start_shoot(current_time)
            self.last_shot_time = current_time
            self.sound_manager.play_sound('gunshot')
            spawn_offset = -100 if self.direction == "left" else 100
            bullet_x = SCREEN_WIDTH // 2 + spawn_offset
            bullet_y = self.rect.centery + 35
            bullet_width = int(100 * BULLET_SCALE)
            bullet_height = int(100 * BULLET_SCALE)
            bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
            initial_velocity = (BULLET_SPEED if self.direction == "right" else -BULLET_SPEED, 0)
            self.bullets.append({
                'rect': bullet_rect,
                'velocity': initial_velocity,
                'direction': self.direction
            })
            self.current_bullets -= 1

    def throw(self, current_time: int, velocity: Tuple[float, float]) -> None:
        if (current_time - self.animation.last_throw_time >= self.animation.throw_cooldown and
            not self.animation.throwing and
            not self.animation.reloading and
            self.current_grenades > 0):

            self.animation.start_throw(current_time)

            def delayed_throw():
                spawn_offset = -BULLET_SPAWN_OFFSET if self.direction == "left" else BULLET_SPAWN_OFFSET
                grenade_x = SCREEN_WIDTH // 2 + spawn_offset
                grenade_y = self.rect.centery + 25
                grenade_width = int(20 * BULLET_SCALE * 4)
                grenade_height = int(20 * BULLET_SCALE * 4)

                self.grenades.append({
                    'rect': pygame.Rect(grenade_x, grenade_y, grenade_width, grenade_height),
                    'velocity': velocity,
                    'direction': self.direction,
                    'angle': 0,
                    'rotation_speed': 10,
                    'start_time': current_time,
                    'is_active': True
                })
                self.current_grenades -= 1

            pygame.time.set_timer(pygame.USEREVENT, 500)
            self.delayed_throw_callback = delayed_throw

    def start_reload(self) -> None:
        if not self.animation.reloading and self.current_bullets < self.max_bullets:
            self.animation.start_reload()
            self.reload_complete_time = pygame.time.get_ticks() + (len(self.assets.recharge_frames) * self.animation.throw_frame_delay)

    def handle_jumping(self, keys: pygame.key.ScancodeWrapper) -> None:
        if self.jumping:
            self.rect.y += self.velocity
            self.velocity += GRAVITY
            if self.rect.y >= self.original_y:
                self.rect.y = self.original_y
                self.jumping = False
                self.velocity = 0
        elif keys[pygame.K_w] and not self.jumping:
            self.jumping = True
            self.velocity = JUMP_STRENGTH

    def start_grenade_aim(self, pos: Tuple[int, int]) -> None:
        self.is_aiming_grenade = True
        self.grenade_aim_start_pos = pos
        self.grenade_aim_current_pos = pos
        self.grenade_trajectory_points = []
        self.grenade_power = 0

    def update_grenade_aim(self, pos: Tuple[int, int]) -> None:
        if self.is_aiming_grenade:
            self.grenade_aim_current_pos = pos
            dx = self.grenade_aim_start_pos[0] - self.grenade_aim_current_pos[0]
            dy = self.grenade_aim_start_pos[1] - self.grenade_aim_current_pos[1]
            distance = math.sqrt(dx * dx + dy * dy)
            self.grenade_power = min(distance * PULL_MULTIPLIER, MAX_PULL_DISTANCE * PULL_MULTIPLIER)
            self.grenade_trajectory_points = []
            velocity_x = dx * PULL_MULTIPLIER
            velocity_y = dy * PULL_MULTIPLIER
            x, y = SCREEN_WIDTH // 2, self.rect.centery
            vx, vy = velocity_x, velocity_y
            for _ in range(TRAJECTORY_DOTS * 2):
                self.grenade_trajectory_points.append((x, y))
                x += vx
                y += vy
                vy += GRENADE_GRAVITY

    def release_grenade_aim(self) -> None:
        if self.is_aiming_grenade:
            dx = self.grenade_aim_start_pos[0] - self.grenade_aim_current_pos[0]
            dy = self.grenade_aim_start_pos[1] - self.grenade_aim_current_pos[1]
            velocity = (dx * PULL_MULTIPLIER, dy * PULL_MULTIPLIER)
            self.throw(pygame.time.get_ticks(), velocity)
            self.is_aiming_grenade = False
            self.grenade_trajectory_points = []
            self.grenade_power = 0

    def draw_bullet_counter(self, screen) -> None:
        ammo_bg = pygame.Surface((220, 130), pygame.SRCALPHA)
        for y in range(130):
            alpha = int(150 * (1 - y / 130))
            pygame.draw.line(ammo_bg, (0, 0, 0, alpha), (0, y), (220, y))
        for i in range(3):
            alpha = 100 - i * 30
            pygame.draw.rect(ammo_bg, (255, 255, 255, alpha), (i, i, 220 - i * 2, 130 - i * 2), 2)
        bar_width = 200
        bar_height = 30
        bar_x = (220 - bar_width) // 2
        bar_spacing = 25
        total_content_height = (bar_height * 2) + bar_spacing + 50
        start_y = (130 - total_content_height) // 2 + 10
        bullet_y = start_y + 25
        for y in range(bar_height):
            shade = 30 + (y * 2)
            pygame.draw.line(ammo_bg, (shade, shade, shade, 200),
                           (bar_x, bullet_y + y),
                           (bar_x + bar_width, bullet_y + y))
        current_bullet_width = int((self.current_bullets / self.max_bullets) * bar_width)
        for i in range(3):
            alpha = 200 - i * 50
            pygame.draw.rect(ammo_bg, (255, 215, 0, alpha),
                           (bar_x, bullet_y, current_bullet_width, bar_height))
        pygame.draw.line(ammo_bg, (200, 200, 200, 200), (bar_x, bullet_y), (bar_x + bar_width, bullet_y), 2)
        pygame.draw.line(ammo_bg, (50, 50, 50, 200), (bar_x, bullet_y + bar_height), (bar_x + bar_width, bullet_y + bar_height), 2)
        pygame.draw.line(ammo_bg, (200, 200, 200, 200), (bar_x, bullet_y), (bar_x, bullet_y + bar_height), 2)
        pygame.draw.line(ammo_bg, (50, 50, 50, 200), (bar_x + bar_width, bullet_y), (bar_x + bar_width, bullet_y + bar_height), 2)
        grenade_y = bullet_y + bar_height + bar_spacing
        for y in range(bar_height):
            shade = 30 + (y * 2)
            pygame.draw.line(ammo_bg, (shade, shade, shade, 200),
                           (bar_x, grenade_y + y),
                           (bar_x + bar_width, grenade_y + y))
        current_grenade_width = int((self.current_grenades / self.max_grenades) * bar_width)
        for i in range(3):
            alpha = 200 - i * 50
            pygame.draw.rect(ammo_bg, (255, 50, 50, alpha),
                           (bar_x, grenade_y, current_grenade_width, bar_height))
        pygame.draw.line(ammo_bg, (200, 200, 200, 200), (bar_x, grenade_y), (bar_x + bar_width, grenade_y), 2)
        pygame.draw.line(ammo_bg, (50, 50, 50, 200), (bar_x, grenade_y + bar_height), (bar_x + bar_width, grenade_y + bar_height), 2)
        pygame.draw.line(ammo_bg, (200, 200, 200, 200), (bar_x, grenade_y), (bar_x, grenade_y + bar_height), 2)
        pygame.draw.line(ammo_bg, (50, 50, 50, 200), (bar_x + bar_width, grenade_y), (bar_x + bar_width, grenade_y + bar_height), 2)
        bullet_label = self.font.render("AMMO", True, (255, 255, 255))
        grenade_label = self.font.render("GRENADES", True, (255, 255, 255))
        bullet_count = self.font.render(f"{self.current_bullets}/{self.max_bullets}", True, (255, 255, 255))
        grenade_count = self.font.render(f"{self.current_grenades}/{self.max_grenades}", True, (255, 255, 255))
        shadow_offset = 2
        shadow_color = (0, 0, 0, 150)
        shadow = self.font.render("AMMO", True, shadow_color)
        ammo_bg.blit(shadow, (bar_x + 5 + shadow_offset, bullet_y - 25 + shadow_offset))
        ammo_bg.blit(bullet_label, (bar_x + 5, bullet_y - 25))
        shadow = self.font.render("GRENADES", True, shadow_color)
        ammo_bg.blit(shadow, (bar_x + 5 + shadow_offset, grenade_y - 25 + shadow_offset))
        ammo_bg.blit(grenade_label, (bar_x + 5, grenade_y - 25))
        shadow = self.font.render(f"{self.current_bullets}/{self.max_bullets}", True, shadow_color)
        ammo_bg.blit(shadow, (bar_x + bar_width - bullet_count.get_width() - 5 + shadow_offset,
                            bullet_y - 25 + shadow_offset))
        ammo_bg.blit(bullet_count, (bar_x + bar_width - bullet_count.get_width() - 5, bullet_y - 25))
        shadow = self.font.render(f"{self.current_grenades}/{self.max_grenades}", True, shadow_color)
        ammo_bg.blit(shadow, (bar_x + bar_width - grenade_count.get_width() - 5 + shadow_offset,
                            grenade_y - 25 + shadow_offset))
        ammo_bg.blit(grenade_count, (bar_x + bar_width - grenade_count.get_width() - 5, grenade_y - 25))
        screen.blit(ammo_bg, (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 140))

    def draw_health_bar(self, screen) -> None:
        bar_x = SCREEN_WIDTH - self.health_bar_width - self.health_bar_padding
        bar_y = self.health_bar_padding
        pygame.draw.rect(screen, MILITARY_RED,
                        (bar_x, bar_y, self.health_bar_width, self.health_bar_height))
        current_width = int((self.current_health / self.max_health) * self.health_bar_width)
        pygame.draw.rect(screen, CAMO_GREEN,
                        (bar_x, bar_y, current_width, self.health_bar_height))
        pygame.draw.rect(screen, WHITE,
                        (bar_x, bar_y, self.health_bar_width, self.health_bar_height), 2)

    def draw_grenade_aim(self, screen) -> None:
        if not self.is_aiming_grenade:
            return
        sight_radius = 20
        sight_color = (255, 0, 0, 180)
        sight_thickness = 2
        sight_surface = pygame.Surface((sight_radius * 2, sight_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(sight_surface, sight_color, (sight_radius, sight_radius), sight_radius, sight_thickness)
        pygame.draw.line(sight_surface, sight_color,
                        (sight_radius - 10, sight_radius),
                        (sight_radius + 10, sight_radius),
                        sight_thickness)
        pygame.draw.line(sight_surface, sight_color,
                        (sight_radius, sight_radius - 10),
                        (sight_radius, sight_radius + 10),
                        sight_thickness)
        pygame.draw.line(sight_surface, sight_color,
                        (sight_radius - 7, sight_radius - 7),
                        (sight_radius + 7, sight_radius + 7),
                        sight_thickness)
        pygame.draw.line(sight_surface, sight_color,
                        (sight_radius - 7, sight_radius + 7),
                        (sight_radius + 7, sight_radius - 7),
                        sight_thickness)
        screen.blit(sight_surface,
                   (self.grenade_aim_current_pos[0] - sight_radius,
                    self.grenade_aim_current_pos[1] - sight_radius))
        if len(self.grenade_trajectory_points) > 1:
            for i in range(len(self.grenade_trajectory_points) - 1):
                progress = i / len(self.grenade_trajectory_points)
                alpha = int(255 * (1 - progress))
                segment_surface = pygame.Surface((2, 2), pygame.SRCALPHA)
                segment_surface.fill((255, 255, 255, alpha))
                screen.blit(segment_surface, self.grenade_trajectory_points[i])
        power_bar_width = 200
        power_bar_height = 10
        power_bar_x = SCREEN_WIDTH // 2 - power_bar_width // 2
        power_bar_y = self.rect.y - 30
        pygame.draw.rect(screen, (50, 50, 50),
                        (power_bar_x, power_bar_y, power_bar_width, power_bar_height))
        power_width = int((self.grenade_power / (MAX_PULL_DISTANCE * PULL_MULTIPLIER)) * power_bar_width)
        for x in range(power_width):
            progress = x / power_bar_width
            color = (
                int(255 * (1 - progress)),
                int(255 * progress),
                0,
                255
            )
            pygame.draw.line(screen, color,
                           (power_bar_x + x, power_bar_y),
                           (power_bar_x + x, power_bar_y + power_bar_height))
        pygame.draw.rect(screen, (200, 200, 200),
                        (power_bar_x, power_bar_y, power_bar_width, power_bar_height), 1)


class Zombie:
    """
    Represents a zombie enemy in the game.
    Handles zombie movement, attacks, health, and animations.
    """

    def __init__(self, x: int, y: int, assets: GameAssets):
        # Initialize zombie position and dimensions
        self.rect = pygame.Rect(x + 40, y + 100, 60, 140)  # Hitbox for collision detection

        # Game assets and animation
        self.assets = assets  # Game assets (sprites, animations)
        self.frame = 0  # Current animation frame
        self.frame_timer = 0  # Timer for frame updates
        self.frame_delay = 150  # Delay between frame updates

        # Movement and behavior
        self.speed = 2  # Movement speed
        self.direction = "left"  # Current facing direction
        self.health = 100  # Current health
        self.max_health = 100  # Maximum health
        self.is_alive = True  # Whether zombie is alive

        # Combat parameters
        self.detection_range = 500  # Range at which zombie detects player
        self.attack_range = 100  # Range at which zombie can attack
        self.health_bar_width = 40  # Width of health bar
        self.health_bar_height = 5  # Height of health bar

        # UI elements
        self.font = pygame.font.Font(None, 20)  # Font for UI elements

        # Attack system
        self.is_attacking = False  # Whether zombie is attacking
        self.attack_frame = 0  # Current attack animation frame
        self.attack_frame_timer = 0  # Timer for attack animation
        self.attack_frame_delay = 100  # Delay between attack frames
        self.attack_cooldown = 1000  # Time between attacks
        self.last_attack_time = 0  # Last time zombie attacked
        self.attack_damage = 10  # Damage per attack
        self.has_dealt_damage = False  # Whether damage was dealt in current attack

    def update(self, player_x: int, player: 'Player') -> None:
        """
        Updates zombie state including movement, attacks, and animations.

        Args:
            player_x (int): X position of the player
            player (Player): Player object for interaction
        """
        if not self.is_alive:
            return

        current_time = pygame.time.get_ticks()
        distance_to_player = abs(self.rect.x - player_x)

        # Handle player detection and attack
        if distance_to_player <= self.detection_range:
            if distance_to_player <= self.attack_range:
                # Attack player if cooldown has passed
                if not self.is_attacking and current_time - self.last_attack_time >= self.attack_cooldown:
                    self.is_attacking = True
                    self.attack_frame = 0
                    self.has_dealt_damage = False
                    self.last_attack_time = current_time

                # Handle attack animation and damage
                if self.is_attacking:
                    if current_time - self.attack_frame_timer >= self.attack_frame_delay:
                        self.attack_frame_timer = current_time
                        self.attack_frame = (self.attack_frame + 1) % len(self.assets.zombie_attack_frames)
                        if not self.has_dealt_damage and self.attack_frame == 0:
                            player.take_damage(self.attack_damage)
                            self.has_dealt_damage = True
                        if self.attack_frame == 0:
                            self.is_attacking = False
            else:
                # Move towards player
                if self.rect.x > player_x:
                    self.rect.x -= self.speed
                    self.direction = "left"
                else:
                    self.rect.x += self.speed
                    self.direction = "right"
                self.is_attacking = False
                self.attack_frame = 0

        # Update walking animation if not attacking
        if not self.is_attacking:
            self.frame_timer += clock.get_time()
            if self.frame_timer > self.frame_delay:
                self.frame_timer = 0
                self.frame = (self.frame + 1) % len(self.assets.zombie_frames)

    def draw(self, screen, world_offset: int) -> None:
        """
        Draws the zombie and its health bar.

        Args:
            screen: Pygame surface to draw on
            world_offset (int): Current world offset for scrolling
        """
        if not self.is_alive:
            return

        screen_x = self.rect.x - world_offset - 40
        if 0 <= screen_x <= SCREEN_WIDTH:
            # Draw zombie sprite
            frame = self.assets.zombie_attack_frames[self.attack_frame] if self.is_attacking else self.assets.zombie_frames[self.frame]
            frame = pygame.transform.flip(frame, self.direction == "left", False)
            screen.blit(frame, (screen_x, self.rect.y - 100))

            # Draw health bar
            health_bar_x = screen_x + (frame.get_width() - self.health_bar_width) // (3 if self.direction == "left" else 3)
            health_bar_y = self.rect.y - 23
            pygame.draw.rect(screen, MILITARY_RED,
                           (health_bar_x, health_bar_y,
                            self.health_bar_width, self.health_bar_height))
            current_width = int((self.health / self.max_health) * self.health_bar_width)
            pygame.draw.rect(screen, CAMO_GREEN,
                           (health_bar_x, health_bar_y,
                            current_width, self.health_bar_height))
            pygame.draw.rect(screen, WHITE,
                           (health_bar_x, health_bar_y,
                            self.health_bar_width, self.health_bar_height), 1)

    def take_damage(self, amount: int) -> None:
        """
        Handles zombie taking damage.

        Args:
            amount (int): Amount of damage to take
        """
        self.health -= amount
        if self.health <= 0:
            self.is_alive = False


class GameOverScreen:
    def __init__(self, screen, clock, is_win: bool):
        self.screen = screen
        self.clock = clock
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_option = 0
        self.options = ["Play Again", "Main Menu"]
        self.fade_alpha = 0
        self.fade_speed = 5
        self.is_win = is_win
        self.stats = {
            "zombies_killed": 0,
            "time_survived": "00:00",
            "distance_traveled": 0,
            "accuracy": 0
        }
        self.military_font = pygame.font.Font(None, 72)
        self.background_image = pygame.image.load("Assets/Background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    def draw_overlay(self, alpha=100):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (0, 0))

    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None, center=True):
        if font is None:
            font = self.font
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_overlay(150)
        if self.is_win:
            primary_color = (255, 215, 0)
            secondary_color = (192, 192, 192)
            title = "MISSION ACCOMPLISHED"
        else:
            primary_color = (129, 97, 60)
            secondary_color = (107, 142, 35)
            title = "MISSION FAILED"
        box_width = 800
        box_height = 400
        box_x = self.screen_width // 2 - box_width // 2
        box_y = self.screen_height // 4 - 100
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        border_width = 3
        pygame.draw.rect(box_surface, primary_color, (0, 0, box_width, box_height), border_width)
        inner_border = 10
        pygame.draw.rect(box_surface, secondary_color, (inner_border, inner_border,
                                                     box_width - 2 * inner_border,
                                                     box_height - 2 * inner_border), 2)
        self.screen.blit(box_surface, (box_x, box_y))
        self.draw_text(title, self.screen_width // 2, self.screen_height // 4 - 50, primary_color, self.military_font)
        stats_y = self.screen_height // 4 + 50
        self.draw_text(f"Zombies Eliminated: {self.stats['zombies_killed']}", self.screen_width // 2, stats_y, WHITE)
        self.draw_text(f"Time Survived: {self.stats['time_survived']}", self.screen_width // 2, stats_y + 40, WHITE)
        self.draw_text(f"Distance Traveled: {self.stats['distance_traveled']}m", self.screen_width // 2, stats_y + 80, WHITE)
        if self.is_win:
            self.draw_text(f"Accuracy: {self.stats['accuracy']}%", self.screen_width // 2, stats_y + 120, WHITE)
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_buttons_height = (len(self.options) * button_height) + ((len(self.options) - 1) * button_spacing)
        start_y = self.screen_height - total_buttons_height - 100
        for i, option in enumerate(self.options):
            button_y = start_y + (i * (button_height + button_spacing))
            button_x = self.screen_width // 2 - button_width // 2
            button_color = primary_color if i == self.selected_option else WHITE
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height), 2)
            self.draw_text(option, button_x + button_width // 2, button_y + button_height // 2, button_color)
        controls = ["↑/↓ to Navigate", "ENTER to Select"]
        for i, control in enumerate(controls):
            self.draw_text(control, self.screen_width // 2, start_y + total_buttons_height + 30 + i * 30, (200, 200, 200))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    selected = self.options[self.selected_option]
                    if selected == "Play Again":
                        return "retry"
                    elif selected == "Main Menu":
                        return "menu"
        return "game_over"

    def run(self):
        while True:
            action = self.handle_events()
            if action != "game_over":
                return action
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)


class LoseScreen(GameOverScreen):
    def __init__(self, screen, clock):
        super().__init__(screen, clock, False)


class IntroCutscene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_width, self.screen_height = screen.get_size()
        self.running = True
        self.current_scene = 0
        self.alpha = 0
        self.fade_speed = 3
        self.scene_duration = 3000
        self.scene_start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.text_complete = False
        self.text_complete_time = 0
        self.text_wait_duration = 1000
        self.military_font = pygame.font.Font(None, 72)
        self.background_image = pygame.image.load("Assets/Background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.sound_manager = SoundManager()
        self.sound_manager.play_music('menu')
        self.scenes = [
            {
                "title": "OPERATION: ZOMBIE STRIKE",
                "subtitle": "TACTICAL SURVIVAL",
                "effect": "fade"
            },
            {
                "title": "MISSION BRIEFING",
                "subtitle": "A deadly virus has turned the population into zombies",
                "effect": "typewriter"
            },
            {
                "title": "YOUR MISSION",
                "subtitle": "Eliminate all threats and survive",
                "effect": "typewriter"
            },
            {
                "title": "EXTRACTION PLAN",
                "subtitle": "A military tank will arrive to extract you after clearing the area",
                "effect": "typewriter"
            },
            {
                "title": "PREPARE FOR DEPLOYMENT",
                "subtitle": "Good luck, soldier",
                "effect": "fade"
            }
        ]
        self.current_text = ""
        self.target_text = ""
        self.typewriter_speed = 2
        self.typewriter_index = 0
        self.typewriter_timer = 0

    def draw_overlay(self, alpha=100):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (0, 0))

    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None, center=True):
        if font is None:
            font = self.font
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_scene(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_overlay(150)
        current_scene = self.scenes[self.current_scene]
        box_width = 800
        box_height = 300
        box_x = self.screen_width // 2 - box_width // 2
        box_y = self.screen_height // 2 - box_height // 2
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        border_width = 3
        pygame.draw.rect(box_surface, (255, 255, 255, 100), (0, 0, box_width, box_height), border_width)
        self.screen.blit(box_surface, (box_x, box_y))
        self.draw_text(current_scene["title"], self.screen_width // 2, box_y + 80, HIGHLIGHT, self.military_font)
        if current_scene["effect"] == "typewriter":
            self.draw_text(self.current_text, self.screen_width // 2, box_y + 180, WHITE, self.font)
        else:
            self.draw_text(current_scene["subtitle"], self.screen_width // 2, box_y + 180, WHITE, self.font)
        skip_text = "Press SPACE to skip"
        self.draw_text(skip_text, self.screen_width // 2, self.screen_height - 50, (200, 200, 200))

    def update_typewriter(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.typewriter_timer > 50:
            self.typewriter_timer = current_time
            if self.typewriter_index < len(self.target_text):
                self.current_text += self.target_text[self.typewriter_index]
                self.typewriter_index += 1
            elif not self.text_complete:
                self.text_complete = True
                self.text_complete_time = current_time

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "start_game"
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
            current_scene = self.scenes[self.current_scene]
            if current_scene["effect"] == "typewriter":
                self.update_typewriter()
                if self.text_complete and current_time - self.text_complete_time >= self.text_wait_duration:
                    self.current_scene += 1
                    if self.current_scene >= len(self.scenes):
                        return "start_game"
                    self.current_text = ""
                    self.target_text = self.scenes[self.current_scene]["subtitle"]
                    self.typewriter_index = 0
                    self.text_complete = False
            else:
                if current_time - self.scene_start_time > self.scene_duration:
                    self.current_scene += 1
                    if self.current_scene >= len(self.scenes):
                        return "start_game"
                    self.scene_start_time = current_time
                    self.current_text = ""
                    self.target_text = self.scenes[self.current_scene]["subtitle"]
                    self.typewriter_index = 0
                    self.text_complete = False
            self.draw_scene()
            pygame.display.flip()
            self.clock.tick(60)
        return "start_game"


class Game:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.assets = GameAssets()
        self.sound_manager = SoundManager()
        self.sound_manager.play_music('wave')
        player_height = self.assets.actions["Idle"][0].get_height()
        self.player = Player(SCREEN_WIDTH // 2,
                           SCREEN_HEIGHT - GROUND_HEIGHT - player_height - 48,
                           self.assets.actions["Idle"][0].get_width(),
                           player_height,
                           self.assets,
                           self.sound_manager)
        self.running = True
        self.game_time = datetime(2024, 1, 1, 6, 0)
        self.world_offset = 0
        self.day_progress = 0
        self.current_time = 0
        self.zombies = []
        self.zombies_killed = 0
        self.wave_zombies_killed = 0
        self.current_wave = 1
        self.max_waves = 3
        self.wave_complete = False
        self.wave_start_time = 0
        self.wave_delay = 5000
        self.wave_zombies = {
            1: {"count": 5, "speed": 3, "health": 100},
            2: {"count": 8, "speed": 3.5, "health": 150},
            3: {"count": 12, "speed": 4, "health": 200}
        }
        self.zombies_spawned = 0
        self.start_time = datetime.now()
        self.bullets_fired = 0
        self.bullets_hit = 0
        self.paused = False
        self.exit_button_hovered = False
        self.exit_button_rect = None
        self.next_wave_button_rect = None
        self.next_wave_button_hovered = False
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.start_wave()

    def start_wave(self):
        self.wave_start_time = pygame.time.get_ticks()
        self.zombies_spawned = 0
        self.wave_zombies_killed = 0
        self.wave_complete = False
        self.spawn_zombie()

    def spawn_zombie(self) -> None:
        if self.zombies_spawned < self.wave_zombies[self.current_wave]["count"]:
            spawn_x = self.world_offset + SCREEN_WIDTH + random.randint(100, 300)
            spawn_y = SCREEN_HEIGHT - GROUND_HEIGHT - self.assets.zombie_frames[0].get_height() - 48
            zombie = Zombie(spawn_x, spawn_y, self.assets)
            zombie.speed = self.wave_zombies[self.current_wave]["speed"]
            zombie.health = self.wave_zombies[self.current_wave]["health"]
            zombie.max_health = zombie.health
            self.zombies.append(zombie)
            self.zombies_spawned += 1

    def draw_wave_complete_screen(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        if self.current_wave < self.max_waves:
            self.draw_text("WAVE COMPLETE!", self.screen_width // 2, self.screen_height // 3, HIGHLIGHT, self.title_font)
            stats_y = self.screen_height // 2
            self.draw_text(f"Zombies Eliminated: {self.zombies_killed}", self.screen_width // 2, stats_y, WHITE)
            self.draw_text(f"Accuracy: {int((self.bullets_hit / max(1, self.bullets_fired)) * 100)}%",
                         self.screen_width // 2, stats_y + 40, WHITE)
            button_width = 200
            button_height = 50
            button_x = self.screen_width // 2 - button_width // 2
            button_y = self.screen_height * 2 // 3
            button_color = HIGHLIGHT if self.next_wave_button_hovered else WHITE
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height), 2)
            self.draw_text("Next Wave", button_x + button_width // 2, button_y + button_height // 2, button_color)
            self.next_wave_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        else:
            self.draw_text("MISSION ACCOMPLISHED!", self.screen_width // 2, self.screen_height // 3, HIGHLIGHT, self.title_font)
            stats_y = self.screen_height // 2
            self.draw_text(f"Total Zombies Eliminated: {self.zombies_killed}", self.screen_width // 2, stats_y, WHITE)
            self.draw_text(f"Time Survived: {str(datetime.now() - self.start_time).split('.')[0]}",
                         self.screen_width // 2, stats_y + 40, WHITE)
            self.draw_text(f"Accuracy: {int((self.bullets_hit / max(1, self.bullets_fired)) * 100)}%",
                         self.screen_width // 2, stats_y + 80, WHITE)

    def update_wave(self) -> None:
        current_time = pygame.time.get_ticks()
        if len(self.zombies) == 0 and self.zombies_spawned >= self.wave_zombies[self.current_wave]["count"]:
            if not self.wave_complete:
                self.wave_complete = True
                self.wave_start_time = current_time
        if (len(self.zombies) < 3 and
            self.zombies_spawned < self.wave_zombies[self.current_wave]["count"] and
            not self.wave_complete):
            self.spawn_zombie()

    def update_zombies(self) -> None:
        for zombie in self.zombies[:]:
            zombie.update(SCREEN_WIDTH // 2 + self.world_offset, self.player)
            for bullet in self.player.bullets[:]:
                bullet_world_rect = pygame.Rect(
                    bullet['rect'].x + self.world_offset,
                    bullet['rect'].y,
                    bullet['rect'].width,
                    bullet['rect'].height
                )
                if zombie.is_alive and bullet_world_rect.colliderect(zombie.rect):
                    zombie.take_damage(35)
                    self.player.bullets.remove(bullet)
                    self.bullets_hit += 1
                    break
            for explosion in self.player.explosions:
                # Create a larger hitbox for the explosion while keeping visual size the same
                explosion_rect = pygame.Rect(
                    explosion['pos'][0] - explosion['radius'] - 200,  # Increased from 50 to 200
                    explosion['pos'][1] - explosion['radius'] - 200,  # Increased from 50 to 200
                    explosion['radius'] * 2 + 400,  # Increased from 100 to 400
                    explosion['radius'] * 2 + 400   # Increased from 100 to 400
                )
                if zombie.is_alive and explosion_rect.colliderect(zombie.rect):
                    zombie.take_damage(150)
            if not zombie.is_alive:
                self.zombies.remove(zombie)
                self.zombies_killed += 1
                self.wave_zombies_killed += 1
                if (self.current_wave == self.max_waves and
                    self.wave_zombies_killed >= self.wave_zombies[self.max_waves]["count"]):
                    stats = {
                        "zombies_killed": self.zombies_killed,
                        "time_survived": str(datetime.now() - self.start_time).split('.')[0],
                        "distance_traveled": int(self.world_offset / 100),
                        "accuracy": int((self.bullets_hit / max(1, self.bullets_fired)) * 100)
                    }
                    outro = OutroCutscene(screen, clock, stats, self.assets)
                    outro_complete = False
                    while not outro_complete:
                        self.draw_background()
                        self.draw_time()
                        self.draw_zombies()
                        self.draw_projectiles()
                        self.player.draw_bullet_counter(screen)
                        self.player.draw_health_bar(screen)
                        self.draw_wave_info()
                        action = outro.handle_events()
                        if action != "outro":
                            if action == "retry":
                                self.__init__()
                                return
                            elif action == "menu":
                                return "menu"
                            elif action == "quit":
                                pygame.quit()
                                sys.exit()
                            break
                        result = outro.update()
                        outro.draw()
                        if result == "complete":
                            outro_complete = True
                        pygame.display.flip()
                        self.clock.tick(60)
                    # Show GameOverScreen after outro
                    game_over_screen = GameOverScreen(screen, clock, True)
                    game_over_screen.stats = stats
                    action = game_over_screen.run()
                    if action == "retry":
                        self.__init__()
                        return
                    elif action == "menu":
                        return "menu"
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

    def draw_wave_info(self) -> None:
        info_bg = pygame.Surface((300, 60), pygame.SRCALPHA)
        info_bg.fill((0, 0, 0, 150))
        pygame.draw.rect(info_bg, (255, 255, 255, 100), (0, 0, 300, 60), 2)
        wave_text = f"Wave {self.current_wave}/{self.max_waves}"
        zombies_remaining = self.wave_zombies[self.current_wave]["count"] - self.wave_zombies_killed
        wave_surface = self.font.render(wave_text, True, WHITE)
        zombies_surface = self.font.render(f"Zombies Remaining: {zombies_remaining}", True, WHITE)
        wave_x = (300 - wave_surface.get_width()) // 2
        zombies_x = (300 - zombies_surface.get_width()) // 2
        total_text_height = wave_surface.get_height() + zombies_surface.get_height() + 5
        start_y = (60 - total_text_height) // 2
        bg_x = (self.screen_width - 300) // 2
        bg_y = 20
        screen.blit(info_bg, (bg_x, bg_y))
        screen.blit(wave_surface, (bg_x + wave_x, bg_y + start_y))
        screen.blit(zombies_surface, (bg_x + zombies_x, bg_y + start_y + wave_surface.get_height() + 5))
        if self.wave_complete and self.current_wave < self.max_waves:
            countdown = max(0, (self.wave_delay - (pygame.time.get_ticks() - self.wave_start_time)) // 1000)
            next_wave_text = f"Next Wave in {countdown}s"
            next_wave_surface = self.font.render(next_wave_text, True, HIGHLIGHT)
            countdown_bg = pygame.Surface((250, 40), pygame.SRCALPHA)
            countdown_bg.fill((0, 0, 0, 150))
            pygame.draw.rect(countdown_bg, (255, 255, 0, 100), (0, 0, 250, 40), 2)
            countdown_x = (250 - next_wave_surface.get_width()) // 2
            countdown_y = (40 - next_wave_surface.get_height()) // 2
            screen.blit(countdown_bg, (self.screen_width // 2 - 125, bg_y + 70))
            screen.blit(next_wave_surface, (self.screen_width // 2 - 125 + countdown_x, bg_y + 70 + countdown_y))

    def draw_overlay(self, alpha=100):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (0, 0))

    def draw_pause_overlay(self):
        self.draw_overlay(180)
        self.draw_text("PAUSED", self.screen_width // 2, self.screen_height // 3, HIGHLIGHT, self.title_font)
        button_width = 200
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_y = self.screen_height // 2
        self.exit_button_rect = self.draw_button(button_x, button_y, button_width, button_height,
                                               "Return to Menu", self.exit_button_hovered)
        self.draw_text("Press ESC to resume", self.screen_width // 2, self.screen_height * 2 // 3, TEXT_COLOR)

    def draw_button(self, x, y, width, height, text, hovered):
        button_color = HIGHLIGHT if hovered else TEXT_COLOR
        pygame.draw.rect(screen, button_color, (x, y, width, height), 2)
        self.draw_text(text, x + width // 2, y + height // 2, button_color)
        return pygame.Rect(x, y, width, height)

    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None, center=True):
        if font is None:
            font = self.font
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        speed = PLAYER_RUN_SPEED if keys[pygame.K_LSHIFT] else PLAYER_SPEED
        moving = False
        if keys[pygame.K_d]:
            self.world_offset += speed
            self.player.direction = "right"
            self.player.animation.set_direction("right")
            moving = True
        elif keys[pygame.K_a] and self.world_offset > 0:
            self.world_offset -= speed
            self.player.direction = "left"
            self.player.animation.set_direction("left")
            moving = True
        if not self.player.animation.shooting:
            self.player.animation.set_animation("Run" if keys[pygame.K_LSHIFT] else "Walk" if moving else "Idle")

    def update_time(self) -> None:
        self.game_time += timedelta(hours=HOURS_PER_SECOND)
        if self.game_time.hour >= 24:
            self.game_time = self.game_time.replace(hour=0)
        self.day_progress = (self.game_time.hour + self.game_time.minute / 60) / 24

    def draw_background(self) -> None:
        day_alpha = self._calculate_day_alpha()
        num_backgrounds = 3
        start_x = -(self.world_offset % SCREEN_WIDTH)
        for i in range(num_backgrounds):
            x_pos = start_x + (i * SCREEN_WIDTH)
            day_surface = self.assets.day_bg.copy()
            day_surface.set_alpha(int(255 * day_alpha))
            screen.blit(day_surface, (x_pos, 0))
            night_surface = self.assets.night_bg.copy()
            night_surface.set_alpha(int(255 * (1 - day_alpha)))
            screen.blit(night_surface, (x_pos, -10))

    def _calculate_day_alpha(self) -> float:
        if 18 <= self.game_time.hour < 19:
            return 1 - (self.game_time.minute / 60)
        elif 5 <= self.game_time.hour < 6:
            return self.game_time.minute / 60
        elif 19 <= self.game_time.hour or self.game_time.hour < 5:
            return 0
        return 1.0

    def draw_time(self) -> None:
        time_bg = pygame.Surface((100, 40), pygame.SRCALPHA)
        time_bg.fill((0, 0, 0, 150))
        pygame.draw.rect(time_bg, (255, 255, 255, 100), (0, 0, 100, 40), 2)
        time_str = self.game_time.strftime("%I:%M %p")
        time_surface = self.assets.font.render(time_str, True, WHITE)
        text_x = (100 - time_surface.get_width()) // 2
        text_y = (40 - time_surface.get_height()) // 2
        screen.blit(time_bg, (10, 10))
        screen.blit(time_surface, (10 + text_x, 10 + text_y))

    def draw_projectiles(self) -> None:
        for bullet in self.player.bullets:
            screen.blit(self.assets.bullet, bullet['rect'])
            pygame.draw.rect(screen, MILITARY_RED, bullet['rect'], 3)
            hitbox_surface = pygame.Surface((bullet['rect'].width, bullet['rect'].height), pygame.SRCALPHA)
            hitbox_surface.fill((*MILITARY_RED, 50))
            screen.blit(hitbox_surface, bullet['rect'])
        for grenade in self.player.grenades:
            grenade_img = pygame.image.load("Assets/Grenade.png")
            grenade_img = pygame.transform.scale(grenade_img,
                (int(grenade_img.get_width() * BULLET_SCALE * 4),
                 int(grenade_img.get_height() * BULLET_SCALE * 4)))
            rotated_grenade = pygame.transform.rotate(grenade_img, -grenade['angle'])
            grenade_rect = rotated_grenade.get_rect(center=grenade['rect'].center)
            screen.blit(rotated_grenade, grenade_rect)
        for explosion in self.player.explosions:
            pygame.draw.circle(screen, EXPLOSION_COLOR, explosion['pos'], explosion['radius'])
            inner_surface = pygame.Surface((explosion['radius'] * 2, explosion['radius'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(inner_surface, (*EXPLOSION_COLOR, 128),
                             (explosion['radius'], explosion['radius']),
                             explosion['radius'] * 0.7)
            screen.blit(inner_surface,
                       (explosion['pos'][0] - explosion['radius'],
                        explosion['pos'][1] - explosion['radius']))
            pygame.draw.circle(screen, (255, 255, 255, 50), explosion['pos'], explosion['radius'], 1)

    def draw_zombies(self) -> None:
        for zombie in self.zombies:
            zombie.draw(screen, self.world_offset)

    def draw_game(self) -> None:
        self.current_time = pygame.time.get_ticks()
        self.draw_background()
        self.draw_time()
        self.player.update_projectiles()
        self.player.animation.update(self.current_time, pygame.key.get_pressed())
        self.update_zombies()
        self.draw_zombies()
        self.draw_projectiles()
        self.player.draw_bullet_counter(screen)
        self.player.draw_health_bar(screen)
        if self.player.is_aiming_grenade:
            self.player.draw_grenade_aim(screen)
        self.player.animation.draw(screen, SCREEN_WIDTH // 2, self.player.rect.y)
        self.draw_wave_info()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and not self.paused:
                    self.player.start_reload()
                elif event.key == pygame.K_SPACE and not self.paused:
                    self.player.shoot(pygame.time.get_ticks(), self.world_offset)
                    self.bullets_fired += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.paused and self.exit_button_rect and self.exit_button_rect.collidepoint(event.pos):
                        return "menu"
                    elif self.wave_complete and self.next_wave_button_rect and self.next_wave_button_rect.collidepoint(event.pos):
                        if self.current_wave < self.max_waves:
                            self.current_wave += 1
                            self.start_wave()
                        else:
                            # Show game over screen
                            game_over_screen = GameOverScreen(screen, clock, True)
                            accuracy = int((self.bullets_hit / max(1, self.bullets_fired)) * 100)
                            game_over_screen.stats = {
                                "zombies_killed": self.zombies_killed,
                                "time_survived": str(datetime.now() - self.start_time).split('.')[0],
                                "distance_traveled": int(self.world_offset / 100),
                                "accuracy": accuracy
                            }
                            action = game_over_screen.run()
                            if action == "retry":
                                self.__init__()
                            elif action == "menu":
                                return
                            elif action == "quit":
                                pygame.quit()
                                sys.exit()
                    elif not self.paused:
                        self.player.start_grenade_aim(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not self.paused:
                self.player.release_grenade_aim()
            elif event.type == pygame.MOUSEMOTION:
                if self.paused and self.exit_button_rect:
                    self.exit_button_hovered = self.exit_button_rect.collidepoint(event.pos)
                elif self.wave_complete and self.next_wave_button_rect:
                    self.next_wave_button_hovered = self.next_wave_button_rect.collidepoint(event.pos)
                elif not self.paused and self.player.is_aiming_grenade:
                    self.player.update_grenade_aim(event.pos)
            elif event.type == pygame.USEREVENT and not self.paused:
                if hasattr(self.player, 'delayed_throw_callback'):
                    self.player.delayed_throw_callback()
                    delattr(self.player, 'delayed_throw_callback')
                    pygame.time.set_timer(pygame.USEREVENT, 0)

    def run(self) -> None:
        while self.running:
            keys = pygame.key.get_pressed()
            action = self.handle_events()
            if action == "menu":
                return
            if not self.paused:
                self.handle_input(keys)
                self.player.handle_jumping(keys)
                self.update_time()
                self.update_wave()
                self.draw_game()
                self.draw_wave_info()
                if self.wave_complete:
                    self.draw_wave_complete_screen()
            else:
                self.draw_game()
                self.draw_wave_info()
                self.draw_pause_overlay()
            pygame.display.update()
            self.clock.tick(60)
            if self.player.current_health <= 0:
                lose_screen = LoseScreen(screen, clock)
                lose_screen.stats = {
                    "zombies_killed": self.zombies_killed,
                    "time_survived": str(datetime.now() - self.start_time).split('.')[0],
                    "distance_traveled": int(self.world_offset / 100)
                }
                action = lose_screen.run()
                if action == "retry":
                    self.__init__()
                elif action == "menu":
                    return
                elif action == "quit":
                    pygame.quit()
                    sys.exit()


class OutroCutscene:
    def __init__(self, screen, clock, stats, game_assets):
        self.screen = screen
        self.clock = clock
        self.screen_width, self.screen_height = screen.get_size()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.stats = stats
        self.assets = game_assets
        self.tank_img = pygame.image.load("Assets/Tank.png")
        self.tank_img = pygame.transform.scale(self.tank_img, (600, 300))
        self.tank_x = SCREEN_WIDTH + 600
        self.tank_y = SCREEN_HEIGHT - GROUND_HEIGHT - self.tank_img.get_height() + 19
        self.tank_speed = 8
        self.tank_arrived = False
        self.tank_leaving = False
        self.player_x = SCREEN_WIDTH // 2
        player_sprite = self.assets.actions["Idle"][0]
        self.player_y = SCREEN_HEIGHT - GROUND_HEIGHT - player_sprite.get_height() - 45
        self.player_speed = 8
        self.player_arrived = False
        self.player_entered = False
        self.player_direction = "right"
        self.player_frame = 0
        self.player_frame_timer = 0
        self.player_frame_delay = 75
        self.current_state = "tank_arriving"
        self.state_timer = 0
        self.state_delay = 500

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
        return "outro"

    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None, center=True):
        if font is None:
            font = self.font
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.current_state == "player_walking" and not self.player_arrived:
            self.player_frame_timer += self.clock.get_time()
            if self.player_frame_timer > self.player_frame_delay:
                self.player_frame_timer = current_time
                self.player_frame = (self.player_frame + 1) % len(self.assets.actions["Walk"])
        if self.current_state == "tank_arriving":
            if self.tank_x > SCREEN_WIDTH // 2 + 100:
                self.tank_x -= self.tank_speed
            else:
                if not self.tank_arrived:
                    self.tank_arrived = True
                    self.state_timer = current_time
                elif current_time - self.state_timer >= self.state_delay:
                    self.current_state = "player_walking"
        elif self.current_state == "player_walking":
            if self.player_x < self.tank_x + 50:
                self.player_x += self.player_speed
            else:
                if not self.player_arrived:
                    self.player_arrived = True
                    self.player_entered = True
                    self.state_timer = current_time
                elif current_time - self.state_timer >= self.state_delay:
                    self.current_state = "tank_leaving"
        elif self.current_state == "tank_leaving":
            self.tank_x += self.tank_speed
            if self.tank_x > SCREEN_WIDTH + 600:
                if self.current_state != "complete":
                    self.current_state = "complete"
                    self.state_timer = current_time
                    return "complete"

    def draw(self):
        screen.blit(self.tank_img, (self.tank_x, self.tank_y))
        if not self.player_entered:
            if self.current_state == "player_walking":
                frame = self.assets.actions["Walk"][self.player_frame]
                frame = pygame.transform.flip(frame, self.player_direction == "left", False)
                screen.blit(frame, (self.player_x - frame.get_width() // 2, self.player_y))
            else:
                frame = self.assets.actions["Idle"][0]
                frame = pygame.transform.flip(frame, self.player_direction == "left", False)
                screen.blit(frame, (self.player_x - frame.get_width() // 2, self.player_y))
        if self.current_state == "complete":
            self.draw_text("MISSION COMPLETE", self.screen_width // 2, self.screen_height // 3, HIGHLIGHT, self.title_font)
            self.draw_text("You have been successfully extracted", self.screen_width // 2, self.screen_height // 2, WHITE)


class AboutScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_option = 0
        self.options = ["Back"]
        self.military_font = pygame.font.Font(None, 72)
        self.background_image = pygame.image.load("Assets/Background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    def draw_overlay(self, alpha=100):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (0, 0))

    def draw_text(self, text, x, y, color=TEXT_COLOR, font=None, center=True):
        if font is None:
            font = self.font
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_overlay(150)

        # Draw title
        self.draw_text("ABOUT", self.screen_width // 2, 50, HIGHLIGHT, self.title_font)

        # Draw content box
        box_width = 800
        box_height = 500
        box_x = self.screen_width // 2 - box_width // 2
        box_y = 150
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))
        pygame.draw.rect(box_surface, (255, 255, 255, 100), (0, 0, box_width, box_height), 2)
        self.screen.blit(box_surface, (box_x, box_y))

        # Draw content
        content = [
            "OPERATION: ZOMBIE STRIKE",
            "",
            "Created by: Aashrith Raj Tatipamula",
            "",
            "Made with:",
            "Python",
            "Pygame",
            "Visual Studio Code",
            "",
            "For: Mrs. Ellacott's ICS3U Class",
            "",
            "© 2024 Aashrith Games",
            "All Rights Reserved",
            "",
            "Version 1.0.0"
        ]

        y_offset = box_y + 50
        for line in content:
            if line.startswith("•"):
                self.draw_text(line, box_x + 50, y_offset, WHITE, self.small_font, False)
            else:
                self.draw_text(line, self.screen_width // 2, y_offset, WHITE, self.small_font)
            y_offset += 30

        # Draw back button
        button_width = 200
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_y = self.screen_height - 100
        button_color = HIGHLIGHT if self.selected_option == 0 else WHITE
        pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height), 2)
        self.draw_text("Back", button_x + button_width // 2, button_y + button_height // 2, button_color)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_RETURN:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button_width = 200
                    button_height = 50
                    button_x = self.screen_width // 2 - button_width // 2
                    button_y = self.screen_height - 100
                    back_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                    if back_button_rect.collidepoint(event.pos):
                        return "menu"
        return "about"

    def run(self):
        while True:
            action = self.handle_events()
            if action != "about":
                return action
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)


def main():
    homepage = HomePage(screen, clock)
    while True:
        action = homepage.run()
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "start_game":
            intro = IntroCutscene(screen, clock)
            action = intro.run()
            if action == "quit":
                pygame.quit()
                sys.exit()
            elif action == "start_game":
                intro.sound_manager.stop_music()
                game = Game()
                action = game.run()
                if action == "menu":
                    homepage = HomePage(screen, clock)
                    continue
        elif action == "instructions":
            pass
        elif action == "settings":
            pass


if __name__ == "__main__":
    main()
