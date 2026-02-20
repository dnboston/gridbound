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

        self.player_tile_x = int(self.player_pos.x // TILE_SIZE)
        self.player_tile_y = int(self.player_pos.y // TILE_SIZE)

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

                # Check map collision
                if self.map_data[target_y][target_x] == 0:
                    self.player_tile_x = target_x
                    self.player_tile_y = target_y
                    self.turn_count += 1

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

        pygame.draw.rect(self.screen, PLAYER_COLOR, pygame.Rect(self.player_pos.x - PLAYER_SIZE // 2,
                                                                self.player_pos.y - PLAYER_SIZE // 2,
                                                                PLAYER_SIZE,
                                                                PLAYER_SIZE,
                                                                )
                        )
        
        turn_surface = self.font.render(f"Turn: {self.turn_count}", True, (255, 255, 255))
        
        self.screen.blit(turn_surface, (10, 10))

        for x in range(0, WINDOW_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))

        for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

        pygame.display.flip()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
