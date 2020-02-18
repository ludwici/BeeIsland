import pygame

from enum import Enum
from pygame.sprite import Sprite


class FlowersData(Enum):
    YELLOW = 1
    RED = 2
    BLUE = 3
    GREEN = 4


class Flower(Sprite):
    def __init__(self, position: (int, int), color: FlowersData) -> None:
        Sprite.__init__(self)
        self.color = color
        self.image = pygame.image.load("../res/images/flowers/{0}.png".format(self.color.value)).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
