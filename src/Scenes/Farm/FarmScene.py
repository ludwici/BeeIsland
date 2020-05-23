import pygame
from pygame.event import Event

from Scenes.Farm.ModifyMenu import ModifyMenu
from UI.RadioGroup import RadioGroup
from src import Constants
from src.Scenes.Scene import Scene
from src.UI.BeeNestButton import BeeNestButton
from src.UI.Button import Button, ButtonEventType, ButtonState


class FarmScene(Scene):
    def __init__(self, main_window, name, player) -> None:
        Scene.__init__(self, main_window=main_window, player=player, name=name)
        self.main_image = pygame.image.load("../res/images/farm1.jpg").convert()
        self.bg_image = pygame.image.load("../res/images/farm1_bg.jpg").convert()
        self.main_image_rect = self.main_image.get_rect()
        self.main_image_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)
        self.to_map_button = Button(parent=self, normal_image_path="../res/images/buttons/to_map_normal.png",
                                    position=(0, 0))
        self.to_map_button.set_image_by_state(ButtonState.HOVERED, "../res/images/buttons/to_map_hover.png")

        self.to_upgrade_button = Button(parent=self, normal_image_path="../res/images/buttons/to_upgrade_normal.png",
                                        position=(0, 100))
        self.to_upgrade_button.set_image_by_state(ButtonState.HOVERED, "../res/images/buttons/to_upgrade_hover.png")

        self.to_map_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.main_window.change_scene("Map")})
        self.to_upgrade_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.show_modify()})
        bg_x = self.main_image_rect.x
        bg_y = self.main_image_rect.y
        positions = [(194, 104), (501, 104), (111, 340), (584, 340), (194, 577), (501, 577)]
        self.nest_group = RadioGroup()
        for i in range(6):
            bee_nest = BeeNestButton(parent=self, normal_image_path="../res/images/bee/hive/hive1_empty_normal.png",
                                     state=ButtonState.NORMAL, group=self.nest_group,
                                     position=(bg_x + positions[i][0], bg_y + positions[i][1]))
            bee_nest.set_image_by_state(ButtonState.HOVERED, "../res/images/bee/hive/hive1_empty_hover.png")

    def show_modify(self):
        m = ModifyMenu(parent=self)
        self.add_drawable(m)

    def update(self, dt: float) -> None:
        [d.update(dt) for d in self._drawable_list]

    def handle_events(self, event: Event) -> None:
        self.nest_group.handle_event(event)
        [d.handle_event(event) for d in self._drawable_list]
        self.to_map_button.handle_event(event)
        self.to_upgrade_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.bg_image, self.bg_image.get_rect())
        surface.blit(self.main_image, self.main_image_rect)
        self.nest_group.draw(surface)
        [d.draw(surface) for d in self._drawable_list]
        self.to_map_button.draw(surface)
        self.to_upgrade_button.draw(surface)

    def on_scene_started(self) -> None:
        super().on_scene_started()
