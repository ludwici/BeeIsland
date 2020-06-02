from copy import copy

import pygame

from src.Quests import Quest
from src.Scenes.Map import MapScene
from src.UI.Button import ButtonEventType, Button, ButtonState


class MapZone(Button):
    __slots__ = (
        "name", "parent", "__is_lock", "quest_label", "quest_list", "quest_icons")

    def __init__(self, parent: MapScene, name: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        normal_image_path = "zones/normal_{0}.png".format(name)
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path, position=position, state=state)
        self.name = name
        self.parent = parent
        self.set_image_by_state(ButtonState.LOCKED, "zones/border_{0}.png".format(name))
        self.lock()
        self.quest_list = []
        self.quest_icons = []

        self._click_rect = copy(self._rect)
        self._click_rect.height -= 30
        self._click_rect.width -= 50
        self._click_rect.x += 35

    def add_quest(self, quest: Quest) -> None:
        quest.icon_btn.parent = quest
        quest.zone = self
        quest.icon_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.parent.show_quest_menu(quest)})
        self.quest_list.append(quest)
        self.quest_icons.append(quest.icon_btn)

    def add_quests(self, quest_list: list) -> None:
        self.quest_list.extend(quest_list)

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if not self.is_locked:
            [qi.handle_event(event) for qi in self.quest_icons]

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if not self.is_locked:
            [qi.draw(screen) for qi in self.quest_icons]
