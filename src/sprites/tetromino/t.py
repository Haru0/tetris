import pygame

from src.sprites.tetromino.base import Base


class T(Base):

    def __init__(self) -> None:
        super().__init__(color=(170, 85, 0))

    def get_shape(self) -> pygame.Surface:
        shape = pygame.Surface((3, 2))
        shape.set_colorkey((0, 0, 0))

        pygame.draw.rect(shape, self.color, ((0, 0), (3, 1)))
        pygame.draw.rect(shape, self.color, ((1, 1), (1, 1)))

        return shape
