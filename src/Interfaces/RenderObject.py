from abc import ABC, abstractmethod

import pygame
from pygame.rect import Rect

# TODO: Template pattern
from src.Utils import resource_path


class RenderObject(ABC):
    __slots__ = ("parent", "_rect", "_res_dir", "__is_draw")

    def __init__(self, parent, position: (int, int) = (0, 0)) -> None:
        self._res_dir = resource_path("res/images")
        self.parent = parent
        self._rect = Rect((0, 0, 0, 0))
        self._rect.x = position[0]
        self._rect.y = position[1]
        self.__is_draw = True

    @property
    def position(self) -> (int, int):
        return self._rect.x, self._rect.y

    @property
    def is_draw(self) -> bool:
        return self.__is_draw

    @property
    def size(self) -> (int, int):
        return self._rect.width, self._rect.height

    def show(self) -> None:
        self.__is_draw = True

    def hide(self) -> None:
        self.__is_draw = False

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
