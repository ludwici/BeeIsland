import pygame
from abc import ABC, abstractmethod
from src.Windows import RenderWindow
from pygame.rect import Rect


class Drawable(ABC):
    def __init__(self, parent: RenderWindow, position=Rect((0, 0, 0, 0))) -> None:
        self.parent = parent
        self.rect = position  # TODO: add abstract getter
        self.color = (0, 0, 0)

    def setPosition(self, position) -> None:
        self.rect.x = position.x
        self.rect.y = position.y

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
