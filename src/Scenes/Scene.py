import pygame

from abc import ABC, abstractmethod
from src.Interfaces import Drawable

from pygame.event import Event


class Scene(ABC):
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self._drawable_list = []

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def handle_events(self, event: Event) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    @abstractmethod
    def on_scene_change(self):
        self._drawable_list.clear()

    def add_drawable(self, d: Drawable) -> None:
        self._drawable_list.append(d)

    def remove_drawable(self, d: Drawable) -> None:
        if d in self._drawable_list:
            self._drawable_list.remove(d)
