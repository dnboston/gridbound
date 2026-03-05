import pygame
import random

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BACKGROUND_COLOR,
    TILE_SIZE
)

GRID_WIDTH = WINDOW_WIDTH // TILE_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // TILE_SIZE


PLAYER_COLOR = (200, 200, 200)
PLAYER_SIZE = 20
PLAYER_SPEED = 200

FLOOR_COLOR = (40, 40, 40)
WALL_COLOR = (100, 100, 100)

GOAL_COLOR = (0, 150, 0)

ENEMY_COLOR = (200, 50, 50)


def snap_to_grid(value: float, tile_size: int) -> float:
    return round((value - tile_size / 2) / tile_size) * tile_size + tile_size / 2


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.font = pygame.font.SysFont(None, 24)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gridbound")

        self.clock = pygame.time.Clock()
        self.running = True

        self.keys = pygame.key.get_pressed()

        self.player_pos = pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.reset_game()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            dt = self.clock.tick(FPS) / 1000
            self.update(dt)
            self.render()

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                    return
                
                if self.game_won or self.game_over:
                    return
                
                target_x = self.player_tile_x
                target_y = self.player_tile_y

                if event.key == pygame.K_w:
                    target_y -= 1
                elif event.key == pygame.K_s:
                    target_y += 1
                elif event.key == pygame.K_a:
                    target_x -= 1
                elif event.key == pygame.K_d:
                    target_x += 1

                # Movement block
                enemy = next((e for e in self.enemies if (e["x"], e["y"]) == (target_x, target_y)), None)

                if enemy is not None:
                    damage = random.randint(1, 2)
                    enemy["hp"] -= damage
                    print(f"You deal {damage}! Enemy HP: {enemy['hp']}")
                    self.turn_count += 1

                    if enemy["hp"] <= 0:
                        print("Enemy defeated!")
                        self.enemies.remove(enemy)

                        self.player_xp += 1
                        print(f"XP Gained! ({self.player_xp}/{self.xp_to_next_level})")

                        if self.player_xp >= self.xp_to_next_level:
                            self.level_up()
                    
                    self.move_enemies()

                elif self.map_data[target_y][target_x] != 1:
                    self.player_tile_x = target_x
                    self.player_tile_y = target_y
                    self.turn_count += 1
                    self.move_enemies()

                # Win check
                if (self.player_tile_x, self.player_tile_y) == self.goal_pos:
                    self.game_won = True
                    print("You've reached the goal!")

        self.keys = pygame.key.get_pressed()

    def update(self, dt: float) -> None:
        self.player_pos.x = max(PLAYER_SIZE // 2, min(WINDOW_WIDTH - PLAYER_SIZE // 2, self.player_pos.x))
        self.player_pos.y = max(PLAYER_SIZE // 2, min(WINDOW_HEIGHT - PLAYER_SIZE // 2, self.player_pos.y))

        self.player_pos.x = snap_to_grid(self.player_pos.x, TILE_SIZE)
        self.player_pos.y = snap_to_grid(self.player_pos.y, TILE_SIZE)

        self.player_pos.x = self.player_tile_x * TILE_SIZE + TILE_SIZE / 2
        self.player_pos.y = self.player_tile_y * TILE_SIZE + TILE_SIZE / 2

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile_value = self.map_data[y][x]

                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                if tile_value == 0:
                    pygame.draw.rect(self.screen, FLOOR_COLOR, rect)
                elif tile_value == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                elif tile_value == 2:
                    pygame.draw.rect(self.screen, GOAL_COLOR, rect)

        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (200, 50, 50), (enemy["x"] * TILE_SIZE, enemy["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.draw.rect(self.screen, PLAYER_COLOR, pygame.Rect(self.player_pos.x - PLAYER_SIZE // 2,
                                                                self.player_pos.y - PLAYER_SIZE // 2,
                                                                PLAYER_SIZE,
                                                                PLAYER_SIZE,
                                                                )
                        )
        
        turn_surface = self.font.render(f"Turn: {self.turn_count}", True, (255, 255, 255))
        self.screen.blit(turn_surface, (10, 10))

        hp_surface = self.font.render(f"HP: {self.player_hp}", True, (255, 100, 100))
        self.screen.blit(hp_surface, (10, 30))

        level_surface = self.font.render(f"Level: {self.player_level}", True, (200, 200, 255))
        self.screen.blit(level_surface, (10, 50))

        xp_surface = self.font.render(f"XP: {self.player_xp}/{self.xp_to_next_level}", True, (200, 255, 200))
        self.screen.blit(xp_surface, (10, 70))

        if self.game_won:
            win_surface = self.font.render("YOU WIN", True, (255, 215, 0))

            rect = win_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT //2))
            self.screen.blit(win_surface, rect)
        
        if self.game_over:
            over_surface = self.font.render("GAME OVER", True, (200, 0, 0))

            rect = over_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(over_surface, rect)

        for x in range(0, WINDOW_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))

        for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

        pygame.display.flip()

    def reset_game(self):
        # Reset player position (center of grid)
        self.player_tile_x = int(self.player_pos.x // TILE_SIZE)
        self.player_tile_y = int(self.player_pos.y // TILE_SIZE)

        # Create empty map
        self.map_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Create border walls
        for x in range(GRID_WIDTH):
            self.map_data[0][x] = 1
            self.map_data[GRID_HEIGHT - 1][x] = 1

        for y in range(GRID_HEIGHT):
            self.map_data[y][0] = 1
            self.map_data[y][GRID_WIDTH - 1] = 1

        # Add random interior walls
        wall_count = 20

        for _ in range(wall_count):
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)

            # Avoid placing wall on player start
            if (x, y) != (self.player_tile_x, self.player_tile_y):
                self.map_data[y][x] = 1

        self.turn_count = 0

        # Place goal tile
        while True:
            goal_x = random.randint(1, GRID_WIDTH - 2)
            goal_y = random.randint(1, GRID_HEIGHT - 2)

            if self.map_data[goal_y][goal_x] == 0 and (goal_x, goal_y) != (self.player_tile_x, self.player_tile_y):
                self.map_data[goal_y][goal_x] = 2
                self.goal_pos = (goal_x, goal_y)
                break

        self.game_won = False
        self.game_over = False

        # Spawn enemy
        while True:
            enemy_x = random.randint(1, GRID_WIDTH - 2)
            enemy_y = random.randint(1, GRID_HEIGHT - 2)

            if (self.map_data[enemy_y][enemy_x] == 0 and (enemy_x, enemy_y) != (self.player_tile_x, self.player_tile_y) and (enemy_x, enemy_y) != self.goal_pos):
                self.enemies = [{"x": 8, "y": 8, "hp": 3}, {"x": 2, "y": 7, "hp": 3}, {"x": 10, "y": 3, "hp": 3}]
                break

        self.player_xp = 0
        self.player_level = 1
        self.xp_to_next_level = 3
        self.player_max_hp = 15
        self.player_hp = self.player_max_hp

    def move_enemies(self):
        if not self.enemies:
            return

        for enemy in self.enemies:
            dx = self.player_tile_x - enemy["x"]
            dy = self.player_tile_y - enemy["y"]

            step_x = 0
            step_y = 0

            # Choose dominant direction
            if abs(dx) > abs(dy):
                step_x = 1 if dx > 0 else -1
            else:
                step_y = 1 if dy > 0 else -1

            target_x = enemy["x"]+ step_x
            target_y = enemy["y"] + step_y

            # Move if not wall and prevent enemies from walking into each other
            if (self.map_data[target_y][target_x] != 1 and (target_x, target_y) != (self.player_tile_x, self.player_tile_y) and not any((e["x"], e["y"]) == (target_x, target_y) for e in self.enemies)):
                enemy["x"] = target_x
                enemy["y"] = target_y

            # Attack if adjacent
            if (abs(enemy["x"] - self.player_tile_x) + abs(enemy["y"] - self.player_tile_y) == 1):
                damage = random.randint(1, 2)
                self.player_hp -= damage
                print(f"Enemy deals {damage} damage! Player HP: {self.player_hp}")

                if self.player_hp <= 0:
                    self.game_over = True
                    print("Game Over!")

    def level_up(self):
        self.player_level += 1
        self.player_xp = 0

        self.player_max_hp += 2
        self.player_hp = min(self.player_hp + 2, self.player_max_hp)

        print(F"Level Up! You are now level {self.player_level}")


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
