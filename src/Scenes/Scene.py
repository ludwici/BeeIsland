from abc import ABC, abstractmethod

import pygame
from pygame.event import Event

from src.Database.Localization import Localization
from src.Interfaces import RenderObject
from src.Player import Player
from src.Utils import resource_path


class Scene(ABC):
    __slots__ = ("main_window", "player", "scene_settings", "_name", "_render_list", "_localization", "_res_dir",
                 "_next_scenes", "prev_scene")

    def __init__(self, main_window, name: str, player: Player) -> None:
        self._res_dir = resource_path("res")
        self.main_window = main_window
        self.player = player
        self._name = name
        self._render_list = []
        self._localization = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def localization(self) -> Localization:
        return self._localization

    def update(self, dt: float) -> None:
        [r.update(dt) for r in self._render_list]

    @abstractmethod
    def handle_events(self, event: Event) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        [r.draw(surface) for r in self._render_list]

    def add_scene(self, scene_name: str, scene: "Scene") -> None:
        self.main_window.add_scene(scene_name=scene_name, scene=scene)

    def change_scene(self, scene_name: str) -> None:
        self.main_window.change_scene(scene_name)

    def on_scene_change(self) -> None:
        self._render_list.clear()

    def on_scene_started(self) -> None:
        self._localization = Localization(path="scenes/{0}".format(self.name))

    def find_child_of(self, child: RenderObject, base: RenderObject) -> RenderObject:
        for r in self._render_list:
            if issubclass(type(child), base):
                return r
        return None

    def find_render_by_type(self, t: RenderObject) -> RenderObject:
        for r in self._render_list:
            if type(r) is t:
                return r
        return None

    def add_render(self, r: RenderObject) -> None:
        self._render_list.append(r)

    def remove_render(self, r: RenderObject) -> None:
        if r in self._render_list:
            self._render_list.remove(r)
