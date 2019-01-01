from random import choice

from pygame.sprite import AbstractGroup

from src.sprites.tetromino.base import Base
from src.sprites.tetromino.i import I
from src.sprites.tetromino.j import J
from src.sprites.tetromino.l import L
from src.sprites.tetromino.o import O
from src.sprites.tetromino.s import S
from src.sprites.tetromino.t import T
from src.sprites.tetromino.z import Z


class TetrominoFactory(object):
    """
    Tetromino factory responsibility is to **randomly** construct one of available tetromino sprite.
    """

    available = ('I', 'J', 'L', 'O', 'S', 'T', 'Z')

    def randomize(self, frozen_tetrominos_layer: AbstractGroup) -> Base:
        tetromino_class = globals()[choice(self.available)]

        tetromino = tetromino_class()
        tetromino._frozen_tetrominos_layer = frozen_tetrominos_layer

        return tetromino
