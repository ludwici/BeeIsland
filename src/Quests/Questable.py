from abc import ABC

from Quests.QuestTemplate import QuestTemplate
from Scenes.Map.QuestPopup import QuestPopup
from src import Player
from src.UI.QuestIcon import QuestIcon


class Questable(ABC):
    def __init__(self, quest_template: QuestTemplate, icon_offset: (int, int)) -> None:
        self.__is_allow = False
        self.title = quest_template.title
        self._description = quest_template.desc
        self.zone = None
        self.condition = None
        self.rewards = quest_template.resources_bag
        self.difficult = None
        icon_pos = quest_template.icon_pos[0] + icon_offset[0], quest_template.icon_pos[1] + icon_offset[1]
        self.icon_btn = QuestIcon(parent=self.zone, normal_image_path="../res/images/quest_icon1.png",
                                  position=icon_pos)

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
        QuestPopup.create(scene=self.zone.parent, quest=self)

    def check_allow(self) -> bool:
        self.__is_allow = self.condition
        return self.__is_allow

    def give_rewards_to_player(self, player: Player) -> None:
        player.resources += self.rewards
