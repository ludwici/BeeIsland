from enum import Enum

import pygame
from pygame.sprite import Sprite

from src.Utils import resource_path


class FlowersData(Enum):
    YELLOW = 1
    PURPLE = 2
    BLUE = 3
    GREEN = 4
    TURQUOISE = 5


class Flower(Sprite):
    __slots__ = ("color", "image", "rect")

    def __init__(self, position: (int, int), color: FlowersData) -> None:
        Sprite.__init__(self)
        self.color = color
        self.image = pygame.image.load(
            "{0}/flowers/{1}.png".format(resource_path("res/images"), self.color.value)).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
