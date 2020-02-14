import pygame
from abc import ABC, abstractmethod
from pygame.rect import Rect


class Drawable(ABC):
    def __init__(self, parent, position: (int, int)) -> None:
        self.parent = parent
        self._rect = Rect((0, 0, 0, 0))
        self.setPosition(position)
        self.color = (0, 0, 0)

    @property
    def position(self) -> (int, int):
        return self._rect.x, self._rect.y

    def setPosition(self, position: (int, int)) -> None:
        self._rect.x = position[0]
        self._rect.y = position[1]

    @abstractmethod
    def update(self, dt) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
