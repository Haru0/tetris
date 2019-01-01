import pygame
from pygame import Surface
from pygame.sprite import Group, AbstractGroup

from src.config import Config
from src.sprites.collision_block import CollisionBlock
from src.sprites.frozen_tetrominos import FrozenTetrominos
from src.sprites.tetromino_factory import TetrominoFactory


class Board(Surface):
    """
    Board responsibility is to:
        - create new tetromino when necessary
        - check line collisions and remove completed lines
    """

    width = 10
    height = 20

    collision_groups = []
    tetromino_layer: AbstractGroup
    frozen_tetrominos_layer: AbstractGroup

    def __init__(self):
        super().__init__(self.size)
        self.generate_collision_groups()

    @property
    def size(self) -> object:
        config = Config()
        return config.width, config.height

    def draw(self, screen: Surface) -> None:
        for collision_group in self.collision_groups:
            collision_group.draw(screen)

        self.frozen_tetrominos_layer.draw(screen)
        self.tetromino_layer.draw(screen)

        return

    def update(self, screen: Surface, background: Surface, seconds, drop, pull, rotation, direction) -> None:
        index = self.check_lines()

        self.tetromino_layer.clear(screen, background)

        self.frozen_tetrominos_layer.clear(screen, background)
        self.frozen_tetrominos_layer.draw(screen)

        if index:
            self.clear_line(screen, index)

        self.tetromino_layer.update(seconds, drop, pull, rotation, direction)
        self.tetromino_layer.draw(screen)

        self.add_tetromino()

        return

    def add_tetromino(self) -> None:
        if not self.is_tetromino_necessary:
            return

        tetromino = self.create_tetromino()
        self.tetromino_layer.add(tetromino)

        if tetromino.collides:
            raise Exception("Game over")

        return

    def create_tetromino(self):
        return TetrominoFactory().randomize(self.frozen_tetrominos_layer)

    @property
    def is_tetromino_necessary(self) -> bool:
        """
        See if there is no more sprites under working layer.
        """
        return 0 == len(self.tetromino_layer)

    def check_lines(self):
        """
        Detect collisions and yield first colliding line index.
        """

        for index, collision_group in enumerate(self.collision_groups):
            collisions = pygame.sprite.groupcollide(
                collision_group,
                self.frozen_tetrominos_layer,
                False,
                False,
                pygame.sprite.collide_mask
            )

            if 10 > len(collisions):
                continue

            return index

    def clear_line(self, screen: Surface, index: int) -> None:
        """
        Collect all frozen sprites, draw them, remove line, create new frozen sprite.
        """

        above_line = screen.subsurface((0, 0, Config().width, index * Config.scale)).copy()
        screen.blit(above_line, (0, Config.scale))

        self.frozen_tetrominos_layer.empty()
        self.frozen_tetrominos_layer.add(FrozenTetrominos(screen.copy()))

        return

    def generate_collision_groups(self) -> None:
        """
        Create collision blocks for each board row. They are used for completed row detection.
        """

        config = Config()

        for y in range(0, self.height):
            collision_group = Group()

            for x in range(0, self.width):
                collision_group.add(CollisionBlock(x * config.scale, y * config.scale))

            self.collision_groups.append(collision_group)

        return
