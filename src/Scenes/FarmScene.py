import pygame
from pygame.event import Event

from src import Constants
from src.Scenes.Scene import Scene
from src.UI.BeeNestButton import BeeNestButton


class FarmScene(Scene):
    def __init__(self, main_window, player):
        Scene.__init__(self, main_window=main_window, player=player)
        self.bg_image = pygame.image.load("../res/images/farm1.jpg").convert()
        self.bg_image_rect = self.bg_image.get_rect()
        self.bg_image_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)
        self.bee_nest_list = []

    def update(self, dt: float) -> None:
        [d.update(dt) for d in self._drawable_list]

    def handle_events(self, event: Event) -> None:
        [bn.handle_event(event) for bn in self.bee_nest_list]

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.bg_image, self.bg_image_rect)
        [bn.draw(surface) for bn in self.bee_nest_list]
        [d.draw(surface) for d in self._drawable_list]

    def on_scene_started(self) -> None:
        bg_x = self.bg_image_rect.x
        bg_y = self.bg_image_rect.y
        positions = [(194, 104), (501, 104), (111, 340), (584, 340), (194, 577), (501, 577)]
        for i in range(6):
            bee_nest = BeeNestButton(parent=self, path_to_image="../res/images/bee/hive/hive1_empty_normal.png",
                                     hovered_image="../res/images/bee/hive/hive1_empty_hover.png",
                                     position=(bg_x+positions[i][0], bg_y+positions[i][1]))
            self.bee_nest_list.append(bee_nest)

    def on_scene_change(self):
        super().on_scene_change()
