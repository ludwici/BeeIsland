from abc import ABC
from enum import Enum

from pygame.rect import Rect

from src import Player
from src.UI.QuestIcon import QuestIcon
from src.UI.QuestPopup import QuestPopup


class QuestDifficult(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Questable(ABC):
    def __init__(self, icon_position: (int, int), difficult: QuestDifficult, quest_title: str) -> None:
        self.__is_allow = False
        self.title = quest_title
        self._description = "description"
        self.zone = None
        self.condition = None
        self.rewards = []
        self.difficult = difficult
        self.icon_btn = QuestIcon(parent=self.zone, path_to_image="../res/images/quest_icon1.png",
                                  position=icon_position)

    @property
    def is_allow(self) -> bool:
        return self.__is_allow

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value) -> None:
        self._description = value

    def show_popup(self) -> None:
        position = Rect(0, 70, 0, 0)
        QuestPopup.create(scene=self.zone.parent, position=position, quest=self)

    def check_allow(self) -> bool:
        self.__is_allow = self.condition
        return self.__is_allow

    def give_rewards_to_player(self, player: Player) -> None:
        pass
