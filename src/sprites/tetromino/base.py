import pygame
from pygame import Surface
from pygame.sprite import Sprite, AbstractGroup

from src.config import Config


class Base(Sprite):
    """
    Base Tetromino class
        - Check movement collisions
        - Horizontal movement
        - Dropping
        - Rotating
    """

    _color = (0, 0, 0)
    _frozen = False

    _frozen_tetrominos_layer: AbstractGroup

    def __init__(self, color) -> None:
        self._color = color

        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.move_ip(3 * Config.scale, 0)

        self.mask = pygame.mask.from_threshold(self.image, self.color, (1, 1, 1, 255))

        super().__init__()

    @property
    def color(self):
        return self._color

    def get_image(self) -> Surface:
        shape = self.get_shape()
        shape = pygame.transform.scale(shape, tuple(Config.scale * s for s in shape.get_size()))

        return shape

    def get_shape(self) -> Surface:
        raise NotImplemented

    @property
    def frozen(self) -> bool:
        return self._frozen

    def update(self, seconds, drop=False, pull=False, rotation=None, direction=None):
        if self.frozen:
            return

        if drop:
            self.drop()
            return

        if pull:
            self.pull()
            return

        if rotation:
            self.rotate(rotation)

        if direction:
            self.move(direction)

        return

    def drop(self):
        while not self.frozen:
            self.down(False)

            if self.collides:
                self.up(False)
                self.freeze()

                continue

            if self.rect.bottom == Config().height:
                self.freeze()

                continue

        return

    def pull(self):
        self.down(False)

        if self.collides or self.rect.bottom > Config().height:
            self.up(False)
            self.freeze()

        return

    def freeze(self):
        if self.frozen:
            return

        self.remove(self.groups())
        self.add(self._frozen_tetrominos_layer)

        self._frozen = True

        return

    def up(self, check_collision: bool = True) -> None:
        self.rect.move_ip(0, -Config.scale)

        if check_collision and self.collides:
            self.down(False)

    def right(self, check_collision: bool = True) -> None:
        self.rect.move_ip(Config.scale, 0)

        if check_collision and self.collides:
            self.left(False)

    def down(self, check_collision: bool = True) -> None:
        self.rect.move_ip(0, Config.scale)

        if check_collision and self.collides:
            self.up(False)

    def left(self, check_collision: bool = True) -> None:
        self.rect.move_ip(-Config.scale, 0)

        if check_collision and self.collides:
            self.right(False)

    def move(self, direction, check_collision: bool = True) -> None:
        if direction == pygame.K_UP and self.rect.top > 0:
            self.up(check_collision)

        if direction == pygame.K_RIGHT and self.rect.right < Config().width:
            self.right(check_collision)

        if direction == pygame.K_DOWN and self.rect.bottom < Config().height:
            self.down(check_collision)

        if direction == pygame.K_LEFT and self.rect.left > 0:
            self.left(check_collision)

        return

    def rotate_cw(self, check_collision: bool = True) -> None:
        x, y = self.rect.topleft

        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()

        self.rect.topleft = x, y
        self.mask = pygame.mask.from_threshold(self.image, self.color, (1, 1, 1, 255))

        if check_collision and (self.collides or self.out_of_bounds):
            self.rotate_ccw(False)

        return

    def rotate_ccw(self, check_collision: bool = True) -> None:
        x, y = self.rect.topleft

        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_bounding_rect()

        self.rect.topleft = x, y
        self.mask = pygame.mask.from_threshold(self.image, self.color, (1, 1, 1, 255))

        if check_collision and (self.collides or self.out_of_bounds):
            self.rotate_cw(False)

        return

    def rotate(self, rotation, check_collision: bool = True) -> None:
        if rotation == pygame.K_UP:
            self.rotate_ccw(check_collision)

        if rotation == pygame.K_DOWN:
            self.rotate_ccw(check_collision)

        return

    @property
    def collides(self) -> bool:
        """
        Check if tetromino collides with anything else than himself.
        """

        return 1 <= len(pygame.sprite.spritecollide(self, self._frozen_tetrominos_layer, False, pygame.sprite.collide_mask))

    @property
    def out_of_bounds(self) -> bool:
        return self.rect.top < 0 or self.rect.right > Config().width or self.rect.bottom > Config().height or self.rect.left < 0
