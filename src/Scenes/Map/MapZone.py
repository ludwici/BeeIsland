import copy

import pygame

from Quests import Questable
from Scenes.Map import MapScene
from UI.Button import ButtonEventType
from src.UI.PopupNotify import PopupNotify


class MapZone:
    def __init__(self, parent: MapScene, name: str, pos_x: int, pos_y: int, has_fog: bool = True) -> None:
        self.name = name
        self.parent = parent
        self.border_image = pygame.image.load("../res/images/zones/border_{0}.png".format(self.name)).convert_alpha()
        self.__is_lock = True
        self.__zone_rect = self.border_image.get_rect()
        self.__zone_rect.x = pos_x
        self.__zone_rect.y = pos_y
        self.quest_list = []
        self.quest_icons = []

        self.click_rect = copy.copy(self.__zone_rect)
        self.click_rect.height -= 30
        self.click_rect.width -= 50
        self.click_rect.x += 35

        self.__has_fog = has_fog
        self.show_border = False
        self.__fog_rect = None
        try:
            self.fog_image = pygame.image.load("../res/images/zones/fog_{0}.png".format(self.name)).convert_alpha()
            self.__fog_rect = self.fog_image.get_rect()
            self.__fog_rect.center = self.__zone_rect.center
        except pygame.error:
            self.__has_fog = False

    @property
    def is_lock(self) -> bool:
        return self.__is_lock

    def add_quest(self, quest: Questable) -> None:
        quest.icon_btn.parent = quest
        quest.zone = self
        quest.icon_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.parent.show_quest_menu(quest)})
        self.quest_list.append(quest)
        self.quest_icons.append(quest.icon_btn)

    def add_quests(self, quest_list: list) -> None:
        self.quest_list.extend(quest_list)

    def unlock(self) -> None:
        self.__is_lock = False
        self.__has_fog = False

    def on_mouse_over(self) -> None:
        self.show_border = True

    def on_mouse_out(self) -> None:
        self.show_border = False

    def on_click(self) -> None:
        if self.is_lock:
            PopupNotify.create(scene=self.parent, text=self.parent.localization.get_string("locked_zone"))

    def handle_event(self, event) -> None:
        if self.click_rect.collidepoint(pygame.mouse.get_pos()):
            self.on_mouse_over()
        else:
            self.on_mouse_out()

        [qi.handle_event(event) for qi in self.quest_icons]

    def draw(self, screen: pygame.Surface) -> None:
        if self.show_border:
            screen.blit(self.border_image, self.__zone_rect)
        [qi.draw(screen) for qi in self.quest_icons]
        if self.__has_fog:
            screen.blit(self.fog_image, self.__fog_rect)
