import pygame

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BACKGROUND_COLOR,
)


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gridbound")

        self.clock = pygame.time.Clock()
        self.running = True

        self.keys = pygame.key.get_pressed()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.keys = pygame.key.get_pressed()

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
