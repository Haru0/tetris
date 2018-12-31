import pygame

from src.sprites.tetromino.base import Base


class L(Base):

    def __init__(self) -> None:
        super().__init__(color=(170, 0, 170))

    def get_shape(self) -> pygame.Surface:
        shape = pygame.Surface((3, 2))
        shape.set_colorkey((0, 0, 0))

        pygame.draw.rect(shape, self.color, ((0, 0), (3, 1)))
        pygame.draw.rect(shape, self.color, ((0, 1), (1, 1)))

        return shape
