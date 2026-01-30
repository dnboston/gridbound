import pygame

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BACKGROUND_COLOR,
)


PLAYER_COLOR = (200, 200, 200)
PLAYER_SIZE = 20
PLAYER_SPEED = 200


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
            direction = direction.normalize()

        self.player_pos += direction * PLAYER_SPEED * dt

        self.player_pos.x = max(PLAYER_SIZE // 2, min(WINDOW_WIDTH - PLAYER_SIZE // 2, self.player_pos.x))
        self.player_pos.y = max(PLAYER_SIZE // 2, min(WINDOW_HEIGHT - PLAYER_SIZE // 2, self.player_pos.y))

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.screen, PLAYER_COLOR, pygame.Rect(self.player_pos.x - PLAYER_SIZE // 2,
                                                                self.player_pos.y - PLAYER_SIZE // 2,
                                                                PLAYER_SIZE,
                                                                PLAYER_SIZE,
                                                                )
                        )
        
        pygame.display.flip()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
