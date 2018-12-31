import pygame
from pygame import Surface
from pygame.sprite import Sprite, AbstractGroup

from src.config import Config


class Base(Sprite):
    """
        Base tetromino class is handling its behaviour, this is:
            - check movement collisions
            - horizontal movement
            - dropping
            - rotating
    """

    _color = (0, 0, 0)
    _frozen = False

    _collision_group: AbstractGroup
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

    def update(self, seconds, drop=False, push_down=False, rotation=None, direction=None):
        if self.frozen:
            return

        if drop:
            self.drop()
            return

        if rotation:
            self.rotate(rotation)

        if direction:
            self.move(direction)

    def drop(self):
        while not self._frozen:
            self.move(pygame.K_DOWN, False)

            if self.collides:
                self.move(pygame.K_UP, False)
                self.freeze()
                continue

            if self.rect.bottom == Config().height:
                self.freeze()
                continue

    def freeze(self):
        if not self._frozen:
            self.remove(self.groups())
            self.add(self._frozen_tetrominos_layer)
            self._frozen = True

    def up(self) -> None:
        pass

    def right(self) -> None:
        pass

    def down(self) -> None:
        pass

    def left(self) -> None:
        pass

    def move(self, direction, check_collision: bool = True) -> None:
        if direction == pygame.K_UP and self.rect.top > 0:
            print("move up")
            self.rect.top -= Config.scale

            if check_collision and self.collides:
                self.move(pygame.K_DOWN)

        if direction == pygame.K_RIGHT and self.rect.right < Config().width:
            print("move right")
            self.rect.right += Config.scale

            if check_collision and self.collides:
                self.move(pygame.K_LEFT)

        if direction == pygame.K_DOWN and self.rect.bottom < Config().height:
            print("move down")
            self.rect.bottom += Config.scale

            if check_collision and self.collides:
                self.move(pygame.K_UP)
                # self.freeze()

        if direction == pygame.K_LEFT and self.rect.left > 0:
            print("move left")
            self.rect.left -= Config.scale

            if check_collision and self.collides:
                self.move(pygame.K_RIGHT)

    # def up(self, check_collision: bool = True):
    #     if self.rect.top > 0:
    #         # print("move up")
    #         self.rect.top -= Config.scale
    #
    #         if check_collision and self.collides:
    #             self.freeze()
    #             self.move(pygame.K_DOWN)

    def step(self, check_collision: bool = True):
        # print("move down", self.rect.bottom, Config().height)
        if self.rect.bottom < Config().height:
            self.rect.bottom += Config.scale
        else:
            self.freeze()

        if check_collision and self.collides:
            self.move(pygame.K_UP)
            self.freeze()

    def rotate_cw(self) -> None:
        pass

    def rotate_ccw(self) -> None:
        pass

    def rotate(self, rotation) -> None:
        """
            todo collision & draw bounds -> revert
        """
        if rotation == pygame.K_UP:
            print("Rotate ccw")
            old_x, old_y = self.rect.x, self.rect.y
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_bounding_rect()
            self.rect.x, self.rect.y = old_x, old_y
            self.mask = pygame.mask.from_threshold(self.image, self.color, (1, 1, 1, 255))

        if rotation == pygame.K_DOWN:
            print("Rotate cw")
            old_x, old_y = self.rect.x, self.rect.y
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = old_x, old_y
            self.mask = pygame.mask.from_threshold(self.image, self.color, (1, 1, 1, 255))

    @property
    def collides(self) -> bool:
        """
            Check if tetromino collides with anything else than himself.
        """
        return 1 <= len(
            pygame.sprite.spritecollide(self, self._frozen_tetrominos_layer, False, pygame.sprite.collide_mask))
        # return 1 < len(pygame.sprite.spritecollide(self, self._collision_group, False, pygame.sprite.collide_mask))
