from abc import ABC, abstractmethod

import pygame
from pygame.rect import Rect


class Drawable(ABC):
    def __init__(self, position=Rect((0, 0, 0, 0))) -> None:
        self.rect = position
        self.color = (0, 0, 0)

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
