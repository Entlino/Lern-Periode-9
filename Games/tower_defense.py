import pygame
import math
import random
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Window and Game Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 40
WAVE_DURATION = 1200  # 20 seconds per wave
WAVE_DELAY = 300     # 5 seconds between waves
GAME_START_DELAY = 300  # 5 seconds before first wave

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (30, 144, 255)  # Dodger blue
YELLOW = (218, 165, 32)  # Goldenrod
PURPLE = (147, 112, 219)  # Medium purple
PATH_COLOR = (139, 69, 19)  # Brown path
GRASS_COLOR = (34, 139, 34)  # Forest green
GRID_COLOR = (50, 120, 50)  # Darker green for grid

# Game Configurations
TOWER_TYPES = {
    'Basic': {
        'cost': 100, 
        'range': 150, 
        'damage': 25, 
        'cooldown': 30, 
        'color': BLUE,
        'size': 20,
        'description': 'Balanced tower'
    },
    'Sniper': {
        'cost': 200, 
        'range': 300, 
        'damage': 100, 
        'cooldown': 60, 
        'color': YELLOW,
        'size': 25,
        'description': 'Long range, high damage'
    },
    'Splash': {
        'cost': 150, 
        'range': 120, 
        'damage': 35, 
        'cooldown': 45, 
        'color': PURPLE,
        'size': 22,
        'description': 'Area damage'
    }
}

ENEMY_TYPES = {
    'Normal': {
        'health': 100,
        'speed': 1.5,
        'value': 25,
        'color': RED,
        'size': 15
    },
    'Fast': {
        'health': 50,
        'speed': 3,
        'value': 35,
        'color': GREEN,
        'size': 12
    },
    'Tank': {
        'health': 200,
        'speed': 0.8,
        'value': 50,
        'color': PURPLE,
        'size': 20
    }
}

class Tower:
    def __init__(self, x: int, y: int, tower_type: str):
        self.x = x
        self.y = y
        self.type = tower_type
        self.range = TOWER_TYPES[tower_type]['range']
        self.damage = TOWER_TYPES[tower_type]['damage']
        self.cooldown = TOWER_TYPES[tower_type]['cooldown']
        self.cooldown_timer = 0
        self.level = 1
        self.color = TOWER_TYPES[tower_type]['color']
        self.size = TOWER_TYPES[tower_type]['size']
        self.upgrade_cost = TOWER_TYPES[tower_type]['cost']

    def draw(self, screen):
        # Draw base
        pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y), self.size + 2)
        # Draw tower
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        # Draw level indicator
        font = pygame.font.Font(None, 20)
        level_text = font.render(str(self.level), True, WHITE)
        text_rect = level_text.get_rect(center=(self.x, self.y))
        screen.blit(level_text, text_rect)
        # Draw range circle with transparency
        range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(range_surface, (100, 100, 100, 50), 
                         (self.range, self.range), self.range)
        screen.blit(range_surface, (self.x - self.range, self.y - self.range))

    def upgrade(self):
        self.level += 1
        self.damage *= 1.5
        self.range *= 1.2
        self.cooldown = max(self.cooldown * 0.8, 10)
        self.upgrade_cost *= 2
        self.size += 2

    def can_shoot(self, enemy) -> bool:
        distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
        return distance <= self.range and self.cooldown_timer <= 0

class Enemy:
    def __init__(self, path: List[Tuple[int, int]], enemy_type: str):
        self.path = path
        self.path_index = 0
        self.x = path[0][0]
        self.y = path[0][1]
        self.type = enemy_type
        self.health = ENEMY_TYPES[enemy_type]['health']
        self.max_health = ENEMY_TYPES[enemy_type]['health']
        self.speed = ENEMY_TYPES[enemy_type]['speed']
        self.value = ENEMY_TYPES[enemy_type]['value']
        self.color = ENEMY_TYPES[enemy_type]['color']
        self.size = ENEMY_TYPES[enemy_type]['size']

    def move(self) -> bool:
        if self.path_index >= len(self.path) - 1:
            return False

        target_x, target_y = self.path[self.path_index + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            self.path_index += 1
            if self.path_index >= len(self.path) - 1:
                return False
        else:
            self.x += (dx/distance) * self.speed
            self.y += (dy/distance) * self.speed
        return True

    def draw(self, screen):
        # Draw enemy
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        # Draw health bar with background
        bar_width = 40
        pygame.draw.rect(screen, (50, 50, 50), 
                        (int(self.x) - bar_width//2, int(self.y) - self.size - 10, 
                         bar_width, 5))
        pygame.draw.rect(screen, GREEN, 
                        (int(self.x) - bar_width//2, int(self.y) - self.size - 10, 
                         bar_width * (self.health/self.max_health), 5))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.towers: List[Tower] = []
        self.enemies: List[Enemy] = []
        self.money = 300
        self.lives = 20
        self.wave = 1
        self.enemy_spawn_timer = 0
        self.path = [(0, 300), (300, 300), (300, 100), (500, 100), (500, 500), (800, 500)]
        self.selected_tower = 'Basic'
        # Updated shop buttons with more space
        self.shop_buttons = [
            pygame.Rect(WINDOW_WIDTH - 140, 10, 130, 60),
            pygame.Rect(WINDOW_WIDTH - 140, 80, 130, 60),
            pygame.Rect(WINDOW_WIDTH - 140, 150, 130, 60)
        ]
        self.wave_countdown = GAME_START_DELAY
        self.game_started = False
        self.wave_in_progress = False
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.create_background()

    def create_background(self):
        # Create grass background
        self.background.fill(GRASS_COLOR)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, 40):
            pygame.draw.line(self.background, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.line(self.background, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
        
        # Draw path with better visuals
        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            # Draw path background
            pygame.draw.line(self.background, PATH_COLOR, start, end, 30)
            # Draw path borders
            pygame.draw.line(self.background, BLACK, start, end, 2)  # Changed this line
            # Draw path dots
            distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            steps = int(distance / 20)
            for step in range(steps):
                x = start[0] + (end[0] - start[0]) * step / steps
                y = start[1] + (end[1] - start[1]) * step / steps
                pygame.draw.circle(self.background, BLACK, (int(x), int(y)), 2)

    def spawn_enemy(self):
        # Initial game start
        if not self.game_started:
            if self.wave_countdown > 0:
                self.wave_countdown -= 1
                return
            self.game_started = True
            self.wave_in_progress = True
            self.wave_countdown = WAVE_DURATION
            return

        # Handle wave in progress
        if self.wave_in_progress:
            if len(self.enemies) == 0 and self.enemy_spawn_timer <= 0:
                # All enemies spawned and defeated
                if self.wave_countdown <= 0:
                    self.wave_in_progress = False
                    self.wave += 1
                    self.wave_countdown = WAVE_DELAY
                    self.money += 100  # Wave completion bonus
                    return

            # Spawn new enemies
            if self.enemy_spawn_timer <= 0 and len(self.enemies) < self.wave * 5:
                enemy_type = 'Normal'
                if self.wave >= 3:
                    enemy_type = 'Fast' if random.random() < 0.3 else 'Normal'
                if self.wave >= 5:
                    enemy_type = random.choice(['Normal', 'Fast', 'Tank'])
                self.enemies.append(Enemy(self.path, enemy_type))
                self.enemy_spawn_timer = 60

            self.enemy_spawn_timer -= 1
            self.wave_countdown -= 1

        # Start next wave
        else:
            if self.wave_countdown > 0:
                self.wave_countdown -= 1
            else:
                self.wave_in_progress = True
                self.wave_countdown = WAVE_DURATION
                self.enemy_spawn_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check shop buttons
                for i, button in enumerate(self.shop_buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        self.selected_tower = list(TOWER_TYPES.keys())[i]
                        return True

                # Place tower
                if event.button == 1 and mouse_x < WINDOW_WIDTH - 150:  # Left click
                    tower_cost = TOWER_TYPES[self.selected_tower]['cost']
                    if self.money >= tower_cost:
                        self.towers.append(Tower(mouse_x, mouse_y, self.selected_tower))
                        self.money -= tower_cost
                
                # Upgrade tower
                elif event.button == 3:  # Right click
                    for tower in self.towers:
                        distance = math.sqrt((mouse_x - tower.x)**2 + (mouse_y - tower.y)**2)
                        if distance < tower.size and self.money >= tower.upgrade_cost:
                            self.money -= tower.upgrade_cost
                            tower.upgrade()
        return True

    def update(self):
        # Update enemies
        for enemy in self.enemies[:]:
            if not enemy.move():
                self.lives -= 1
                self.enemies.remove(enemy)
                continue

            if enemy.health <= 0:
                self.money += enemy.value
                self.enemies.remove(enemy)

        # Update towers
        for tower in self.towers:
            if tower.cooldown_timer > 0:
                tower.cooldown_timer -= 1

            for enemy in self.enemies:
                if tower.can_shoot(enemy):
                    enemy.health -= tower.damage
                    tower.cooldown_timer = tower.cooldown
                    break

        # Spawn enemies
        self.spawn_enemy()

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw game objects
        for tower in self.towers:
            tower.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw UI
        font = pygame.font.Font(None, 36)
        money_text = font.render(f"Money: ${self.money}", True, BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        wave_text = font.render(f"Wave: {self.wave}", True, BLACK)
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(wave_text, (10, 70))

        # Draw wave countdown
        if not self.game_started:
            countdown = f"Game starts in: {self.wave_countdown // 60 + 1}"
            text = font.render(countdown, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        elif not self.wave_in_progress and self.wave_countdown > 0:
            countdown = f"Next wave in: {self.wave_countdown // 60 + 1}"
            text = font.render(countdown, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100))
            self.screen.blit(text, text_rect)

        # Draw shop
        shop_bg = pygame.Rect(WINDOW_WIDTH - 150, 0, 150, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, (240, 240, 240), shop_bg)
        pygame.draw.line(self.screen, BLACK, (WINDOW_WIDTH - 150, 0), 
                        (WINDOW_WIDTH - 150, WINDOW_HEIGHT), 2)

        font = pygame.font.Font(None, 24)
        for i, (tower_type, info) in enumerate(TOWER_TYPES.items()):
            button = self.shop_buttons[i]
            # Draw button with hover effect
            mouse_pos = pygame.mouse.get_pos()
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (220, 220, 220), button)
            else:
                pygame.draw.rect(self.screen, WHITE, button)
            pygame.draw.rect(self.screen, BLACK, button, 2)
            
            # Draw tower preview and info
            pygame.draw.circle(self.screen, info['color'], 
                             (button.x + 25, button.y + 30), info['size'])
            name_text = font.render(tower_type, True, BLACK)
            cost_text = font.render(f"${info['cost']}", True, BLACK)
            self.screen.blit(name_text, (button.x + 50, button.y + 10))
            self.screen.blit(cost_text, (button.x + 50, button.y + 35))

        # Draw selected tower info and description
        if self.selected_tower:
            info_text = font.render(f"Selected: {self.selected_tower}", True, BLACK)
            desc_text = font.render(TOWER_TYPES[self.selected_tower]['description'], 
                                  True, BLACK)
            self.screen.blit(info_text, (WINDOW_WIDTH - 140, WINDOW_HEIGHT - 60))
            self.screen.blit(desc_text, (WINDOW_WIDTH - 140, WINDOW_HEIGHT - 30))

        pygame.display.flip()

    def run(self):
        running = True
        while running and self.lives > 0:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()