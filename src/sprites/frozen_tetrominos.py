import pygame
from pygame import Surface
from pygame.sprite import Sprite


class FrozenTetrominos(Sprite):
    """
        Abstract block class representing single tetromino block.
    """

    def __init__(self, image: Surface):
        self.image = image

        self.rect = image.get_rect()
        self.mask = self.get_mask()

        super().__init__()

    def get_mask(self):
        """
            Fake mask of single color image.
        """

        image = self.image.copy()

        for height in range(0, image.get_height()):
            for width in range(0, image.get_width()):
                if (0, 0, 0, 255) != image.get_at((width, height)):
                    image.set_at((width, height), (255, 0, 0, 255))

        return pygame.mask.from_threshold(self.image, (255, 0, 0, 255), (1, 1, 1, 255))
