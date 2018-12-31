import os

import pygame

from src.board import Board
from src.config import Config

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game(object):
    """
        Game responsibility is to:
         - handle main game loop
         - intercept input and pass it to board game object
    """

    score = 0
    speed = 100

    PUSH_DOWN = pygame.USEREVENT + 1

    def __init__(self, width=Config().width, height=Config().height):
        self._screen = pygame.display.set_mode((width, height))

    def init(self):
        pygame.init()
        pygame.display.set_caption("Tetris")

    def run(self):
        pause = False
        running = True

        time_passed = 0.0
        clock = pygame.time.Clock()

        pygame.key.set_repeat(500)
        pygame.time.set_timer(self.PUSH_DOWN, 500)

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

            push_down = drop = False
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

                if event.type == self.PUSH_DOWN:
                    direction = pygame.K_DOWN

            if pause:
                continue

            board.update(
                self._screen,
                background,
                seconds,
                drop,
                push_down,
                rotation,
                direction
            )

            pygame.display.flip()

        pygame.quit()
