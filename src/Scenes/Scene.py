from abc import ABC, abstractmethod

import pygame
from pygame.event import Event

from src.Interfaces import Drawable
from src.Player import Player
from src.QuestSettings import QuestSettings
from src.UI.QuestPopup import QuestPopup


class Scene(ABC):
    def __init__(self, main_window, player: Player) -> None:
        self.main_window = main_window
        self.player = player
        self.scene_settings = QuestSettings()
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
    def on_scene_started(self) -> None:
        pass

    @abstractmethod
    def on_scene_change(self) -> None:
        self._drawable_list.clear()
        QuestPopup.count = 0

    def find_drawable_by_type(self, t) -> Drawable:
        for d in self._drawable_list:
            if type(d) is t:
                return d
        return None

    def add_drawable(self, d: Drawable) -> None:
        self._drawable_list.append(d)

    def remove_drawable(self, d: Drawable) -> None:
        if d in self._drawable_list:
            self._drawable_list.remove(d)
