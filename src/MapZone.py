import copy
from typing import List

import pygame

from src.Interfaces import Questable
from src.Scenes import MapScene
from pygame.rect import Rect

from src.UI.PopupNotify import PopupNotify


class MapZone:
    def __init__(self, parent: MapScene, name: str, pos_x: int, pos_y: int, has_fog: bool = True) -> None:
        self.name = name
        self.parent = parent
        self.border_image = pygame.image.load("../res/images/zones/border_{0}.png".format(self.name)).convert_alpha()
        self.__is_lock = True
        self.zone_rect = self.border_image.get_rect()
        self.zone_rect.x = pos_x
        self.zone_rect.y = pos_y
        self.quest_list = []
        self.quest_icons = []

        self.click_rect = copy.copy(self.zone_rect)
        self.click_rect.height -= 30
        self.click_rect.width -= 50
        self.click_rect.x += 35

        self.has_fog = has_fog
        self.show_border = False
        self.fog_rect = None
        try:
            self.fog_image = pygame.image.load("../res/images/zones/fog_{0}.png".format(self.name)).convert_alpha()
            self.fog_rect = self.fog_image.get_rect()
            self.fog_rect.center = self.zone_rect.center
        except pygame.error:
            self.has_fog = False

    @property
    def is_lock(self) -> bool:
        return self.__is_lock

    def add_quest(self, quest: Questable) -> None:
        quest.icon_btn.parent = quest
        quest.zone = self
        self.quest_list.append(quest)
        self.quest_icons.append(quest.icon_btn)

    def add_quests(self, quest_list: list) -> None:
        self.quest_list.extend(quest_list)

    def unlock(self) -> None:
        self.__is_lock = False
        self.has_fog = False

    def on_mouse_over(self) -> None:
        self.show_border = True

    def on_mouse_out(self) -> None:
        self.show_border = False

    def check_position(self) -> Rect:
        popup_width = 200
        popup_height = 70
        mouse_pos = pygame.mouse.get_pos()
        popup_pos = [0, 0]
        if mouse_pos[0] + popup_width + 20 > self.parent.main_window.size[0]:
            popup_pos[0] = mouse_pos[0] - popup_width
        else:
            popup_pos[0] = mouse_pos[0]

        popup_pos[1] = mouse_pos[1] - popup_height
        if popup_pos[1] < 0:
            popup_pos[1] += popup_height

        correct_position = Rect(popup_pos[0], popup_pos[1], popup_width, popup_height)
        return correct_position

    def on_click(self) -> None:
        if self.is_lock:
            position = self.check_position()
            PopupNotify.create(scene=self.parent, position=position, text="Эта зона ещё не открыта")

    def handle_event(self, event) -> None:
        if self.click_rect.collidepoint(pygame.mouse.get_pos()):
            self.on_mouse_over()
        else:
            self.on_mouse_out()

        [qi.handle_event(event) for qi in self.quest_icons]

    def draw(self, screen: pygame.Surface) -> None:
        if self.show_border:
            screen.blit(self.border_image, self.zone_rect)
        [qi.draw(screen) for qi in self.quest_icons]
        if self.has_fog:
            screen.blit(self.fog_image, self.fog_rect)
