import pygame

from src.sprites.tetromino.base import Base


class I(Base):

    def __init__(self) -> None:
        super().__init__(color=(170, 0, 0))

    def get_shape(self) -> pygame.Surface:
        shape = pygame.Surface((4, 1))
        shape.fill(self.color)

        return shape
