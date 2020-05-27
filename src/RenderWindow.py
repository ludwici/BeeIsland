import os
import traceback

import pygame
from pygame.time import Clock

from Database.Database import Database
from Database.Localization import Localization, LocalList
from Scenes.Farm.FarmScene import FarmScene
from Scenes.Map.MapScene import MapScene
from src.Player import Player
from src.Scenes.Match3.Match3Scene import Match3Scene


class RenderWindow:
    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Bee Island")
        self.__FPS = 60
        self.__size = self.width, self.height = width, height
        self.__screen = pygame.display.set_mode(self.size)

        Localization.set_locale(LocalList.RU)
        self.database = Database()

        self.main_player = Player()
        self.__scene_map = {
            "Map": MapScene(self, name="Map", player=self.main_player),
            "Match3": Match3Scene(self, name="Match3", player=self.main_player),
            "Farm": FarmScene(self, name="Farm", player=self.main_player)
        }
        self.__current_scene = self.__scene_map["Map"]
        self.change_scene("Farm")
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
    def done(self) -> bool:
        return self.__done

    def change_scene(self, scene_name: str, settings=None) -> None:
        self.__prev_scene = self.__current_scene
        self.__current_scene.on_scene_change()
        self.__current_scene = self.__scene_map[scene_name]
        self.__current_scene.scene_settings = settings
        self.__current_scene.on_scene_started()

    def start(self) -> None:
        while not self.done:
            self.loop()
        pygame.quit()
        quit()

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
