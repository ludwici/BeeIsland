from abc import ABC

from src import Player, MapZone
from src.UI.QuestIcon import QuestIcon


class Questable(ABC):
    def __init__(self, zone: MapZone, icon_position: (int, int)) -> None:
        self.__is_allow = False
        self.zone = zone
        self.condition = None
        self.rewards = []

        self.icon_btn = QuestIcon(parent=self.zone.parent, path_to_image="../res/images/quest_icon1.png",
                                  position=icon_position)
        self.zone.quest_list.append(self)
        self.zone.parent.drawable_list.append(self.icon_btn)

    @property
    def is_allow(self) -> bool:
        return self.__is_allow

    def check_allow(self) -> bool:
        self.__is_allow = self.condition
        return self.__is_allow

    def get_rewards_to_player(self, player: Player) -> None:
        pass
