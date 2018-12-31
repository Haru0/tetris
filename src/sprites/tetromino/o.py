import pygame

from src.sprites.tetromino.base import Base


class O(Base):

    def __init__(self) -> None:
        super().__init__(color=(0, 0, 170))

    def get_shape(self) -> pygame.Surface:
        shape = pygame.Surface((2, 2))
        shape.fill(self.color)

        return shape
