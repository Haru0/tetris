from pygame import Surface

from src.sprites.block import Block
from src.config import Config


class CollisionBlock(Block):
    """
    Collision block.
    """

    def __init__(self, x, y):
        self.image = Surface((Config.scale, Config.scale))
        self.image.set_colorkey((10, 20, 30))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.layer = -1

        super().__init__()
