import pygame

from abc import ABC, abstractmethod
from pygame.rect import Rect


class Drawable(ABC):
    def __init__(self, parent, position: (int, int)) -> None:
        self.parent = parent
        self._rect = Rect((0, 0, 0, 0))
        self.set_position(position)
        self.color = (0, 0, 0)

    @property
    def position(self) -> (int, int):
        return self._rect.x, self._rect.y

    def get_size(self) -> (int, int):
        return self._rect.width, self._rect.height

    def set_position(self, position: (int, int)) -> None:
        self._rect.x = position[0]
        self._rect.y = position[1]

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
