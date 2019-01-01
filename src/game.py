import pygame

from src.board import Board
from src.config import Config


class Game(object):
    """
    Main game object, responsible primarily for firing the game. Remaining functionality is:
        - Initialize game objects
        - Handle game loop
        - Intercept input and pass it to Board game object
    """

    speed: int = 500

    PULL: int = pygame.USEREVENT + 1

    def __init__(self, width=Config().width, height=Config().height):
        self._screen = pygame.display.set_mode((width, height))

    def init(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tetris")

    def run(self):
        pause = False
        running = True

        time_passed = 0.0
        clock = pygame.time.Clock()

        pygame.key.set_repeat(500)
        pygame.time.set_timer(self.PULL, self.speed)

        background = pygame.Surface(self._screen.get_size())
        background.fill((0, 0, 0))
        background = background.convert()

        self._screen.blit(background, (0, 0))

        board = Board()
        board.tetromino_layer = pygame.sprite.LayeredUpdates()
        board.frozen_tetrominos_layer = pygame.sprite.LayeredUpdates()

        board.draw(self._screen)

        while running:
            milliseconds = clock.tick(Config.fps)
            seconds = milliseconds / 1000

            if not pause:
                time_passed += seconds

            pull = drop = False
            direction = rotation = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause = not pause

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    rotation = pygame.K_UP

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    direction = pygame.K_RIGHT

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    rotation = pygame.K_DOWN

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    direction = pygame.K_LEFT

                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    drop = True

                if event.type == self.PULL:
                    pull = True

            if pause:
                continue

            board.update(
                self._screen,
                background,
                seconds,
                drop,
                pull,
                rotation,
                direction
            )

            pygame.display.flip()

        pygame.quit()
