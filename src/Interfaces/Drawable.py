from abc import ABC, abstractmethod

import pygame
from pygame.rect import Rect


# TODO: Template pattern
class Drawable(ABC):
    def __init__(self, parent, position: (int, int) = (0, 0)) -> None:
        self.parent = parent
        self._rect = Rect((0, 0, 0, 0))
        self._rect.x = position[0]
        self._rect.y = position[1]
        self.color = (0, 0, 0)

    @property
    def position(self) -> (int, int):
        return self._rect.x, self._rect.y

    # TODO: replace this method to property
    def get_size(self) -> (int, int):
        return self._rect.width, self._rect.height

    def get_rect(self) -> Rect:
        return self._rect

    def set_position(self, position: (int, int)) -> None:
        self._rect.x = position[0]
        self._rect.y = position[1]

    def update(self, dt: float) -> None:
        pass

    def handle_event(self, event) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
