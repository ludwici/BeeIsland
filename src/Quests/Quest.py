from enum import Enum

from src.InGameResources.ResourceBag import ResourceBag
from src.Quests.QuestTemplate import QuestTemplate
from src.UI.Button import Button


class QuestDifficult(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Quest:
    __slots__ = ("time", "score_modifier_percent", "title", "__description", "__zone", "rewards", "difficult",
                 "icon_btn", "bee_list", "additional_rewards", "__q_type", "resources_modifier", "__quest_id")

    def __init__(self, quest_template: QuestTemplate, icon_offset: (int, int)) -> None:
        self.time = 0
        self.__quest_id = quest_template.quest_id
        self.score_modifier_percent = 0
        self.title = quest_template.title
        self.__description = quest_template.desc
        self.resources_modifier = 1
        self.__zone = quest_template.zone_id
        self.bee_list = []
        self.rewards = quest_template.resources_bag
        self.additional_rewards = ResourceBag()
        self.difficult = None
        self.__q_type = quest_template.q_type
        icon_pos = quest_template.icon_pos[0] + icon_offset[0], quest_template.icon_pos[1] + icon_offset[1]
        if self.__q_type == 1:
            icon_name = "quest_icon1.png"
        elif self.__q_type == 4:
            icon_name = "quest_icon4.png"
        else:
            icon_name = "quest_icon1.png"
        self.icon_btn = Button(parent=self, normal_image_path=icon_name, position=icon_pos)

    @property
    def zone(self) -> int:
        return self.__zone

    @property
    def q_type(self) -> int:
        return self.__q_type

    @property
    def quest_id(self) -> int:
        return self.__quest_id

    @property
    def description(self) -> str:
        return self.__description

    def give_rewards_to_player(self, player) -> None:
        player.resources += self.rewards
