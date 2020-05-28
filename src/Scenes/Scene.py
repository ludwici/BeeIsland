from abc import ABC, abstractmethod

import pygame
from pygame.event import Event

from src.Database.Localization import Localization
from src.Interfaces import Drawable
from src.Player import Player
from src.QuestSettings import QuestSettings
from src.Utils import resource_path


# TODO: Adapter pattern
# TODO: Proxy pattern
class Scene(ABC):
    __slots__ = ("main_window", "player", "scene_settings", "_name", "_drawable_list", "_localization", "_res_dir")

    def __init__(self, main_window, name: str, player: Player) -> None:
        self._res_dir = resource_path("res")
        self.main_window = main_window
        self.player = player
        self.scene_settings = QuestSettings()
        self._name = name
        self._drawable_list = []
        self._localization = None

    @property
    def name(self):
        return self._name

    @property
    def localization(self):
        return self._localization

    def update(self, dt: float) -> None:
        [d.update(dt) for d in self._drawable_list]

    @abstractmethod
    def handle_events(self, event: Event) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        [d.draw(surface) for d in self._drawable_list]

    def on_scene_change(self) -> None:
        self._drawable_list.clear()

    def on_scene_started(self) -> None:
        self._localization = Localization(path="scenes/{0}".format(self.name))

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
