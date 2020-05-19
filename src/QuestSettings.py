from enum import Enum

from InGameResources.ResourceBag import ResourceBag


class QuestDifficult(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class QuestSettings:
    def __init__(self) -> None:
        self.difficult = QuestDifficult.EASY
        self.reward_res = ResourceBag()

    def set_difficult(self, difficult: QuestDifficult) -> None:
        self.difficult = difficult
