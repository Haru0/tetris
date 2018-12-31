import pygame

from src.sprites.tetromino.base import Base


class S(Base):

    def __init__(self) -> None:
        super().__init__(color=(0, 170, 0))

    def get_shape(self) -> pygame.Surface:
        shape = pygame.Surface((3, 2))
        shape.set_colorkey((0, 0, 0))

        pygame.draw.rect(shape, self.color, ((1, 0), (2, 1)))
        pygame.draw.rect(shape, self.color, ((0, 1), (2, 1)))

        return shape
