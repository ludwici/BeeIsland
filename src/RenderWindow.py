import os
import sys
import traceback

import pygame
from pygame.time import Clock

from src.Database.Database import Database
from src.Database.Localization import Localization, LocalList
from src.Player import Player
from src.Scenes.Farm.FarmScene import FarmScene
from src.Scenes.Main.MainScene import MainMenuScene
from src.Scenes.Map.MapScene import MapScene
from src.Scenes.Scene import Scene
from src.Utils import resource_path


class RenderWindow:
    __slots__ = (
        "__FPS", "__size", "width", "height", "__screen", "database", "main_player", "__scene_map", "__current_scene",
        "__prev_scene", "__done", "__clock")

    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Bee Island")
        self.__FPS = 60
        self.__size = self.width, self.height = width, height
        self.__screen = pygame.display.set_mode(self.size)
        icon = pygame.image.load("{0}/icon.ico".format(resource_path("res/images/")))
        pygame.display.set_icon(icon)

        Localization.set_locale(LocalList.RU)
        self.database = Database()

        self.main_player = Player()
        self.__scene_map = {
            "Map": MapScene(self, name="Map", player=self.main_player),
            "Farm": FarmScene(self, name="Farm", player=self.main_player),
            "Main": MainMenuScene(self, name="Main", player=self.main_player)
        }
        self.__current_scene = self.__scene_map["Map"]
        self.change_scene("Main")
        self.__prev_scene = None
        self.__done = False
        self.__clock = Clock()

    @property
    def size(self) -> (int, int):
        return self.__size

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @property
    def prev_scene(self) -> Scene:
        return self.__prev_scene

    @property
    def done(self) -> bool:
        return self.__done

    def remove_scene(self, scene_name: str) -> None:
        del self.__scene_map[scene_name]

    def add_scene(self, scene_name: str, scene) -> None:
        self.__scene_map[scene_name] = scene

    def change_scene(self, scene_name: str) -> None:
        self.__prev_scene = self.__current_scene
        self.__current_scene.on_scene_change()
        self.__current_scene = self.__scene_map[scene_name]
        self.__current_scene.on_scene_started()

    def stop(self):
        self.__done = True

    def start(self) -> None:
        while not self.done:
            self.loop()
        pygame.quit()
        sys.exit()

    def change_resolution(self, size: (int, int)) -> None:
        self.__screen = pygame.display.set_mode(size)
        self.__current_scene.on_scene_started()

    def change_lang(self, lang: LocalList) -> None:
        Localization.set_locale(lang)
        self.__current_scene.on_scene_started()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__done = True
            try:
                self.__current_scene.handle_events(event)
            except Exception:
                traceback.print_exc()

    def loop(self) -> None:
        dt = self.__clock.tick(self.__FPS)
        self.handle_events()
        self.__current_scene.update(dt)
        self.__current_scene.draw(surface=self.screen)
        pygame.display.flip()
