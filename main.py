import pygame

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BACKGROUND_COLOR,
    TILE_SIZE
)


PLAYER_COLOR = (200, 200, 200)
PLAYER_SIZE = 20
PLAYER_SPEED = 200


def snap_to_grid(value: float, tile_size: int) -> float:
    return round((value - tile_size / 2) / tile_size) * tile_size + tile_size / 2


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gridbound")

        self.clock = pygame.time.Clock()
        self.running = True

        self.keys = pygame.key.get_pressed()

        self.player_pos = pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

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

        self.keys = pygame.key.get_pressed()

    def update(self, dt: float) -> None:
        is_moving = False

        direction = pygame.Vector2(0, 0)

        if self.keys[pygame.K_w]:
            direction.y -= 1
        if self.keys[pygame.K_s]:
            direction.y += 1
        if self.keys[pygame.K_a]:
            direction.x -= 1
        if self.keys[pygame.K_d]:
            direction.x += 1

        if direction.length_squared() > 0:
            is_moving = True
            direction = direction.normalize()

        self.player_pos += direction * PLAYER_SPEED * dt

        self.player_pos.x = max(PLAYER_SIZE // 2, min(WINDOW_WIDTH - PLAYER_SIZE // 2, self.player_pos.x))
        self.player_pos.y = max(PLAYER_SIZE // 2, min(WINDOW_HEIGHT - PLAYER_SIZE // 2, self.player_pos.y))

        if not is_moving:
            self.player_pos.x = snap_to_grid(self.player_pos.x, TILE_SIZE)
            self.player_pos.y = snap_to_grid(self.player_pos.y, TILE_SIZE)

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.screen, PLAYER_COLOR, pygame.Rect(self.player_pos.x - PLAYER_SIZE // 2,
                                                                self.player_pos.y - PLAYER_SIZE // 2,
                                                                PLAYER_SIZE,
                                                                PLAYER_SIZE,
                                                                )
                        )
        
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
