from src.Quests.QuestTemplate import QuestTemplate
from src.Quests.Questable import Questable


class Match3(Questable):
    def __init__(self, quest_template: QuestTemplate, icon_offset: (int, int)) -> None:
        Questable.__init__(self, quest_template=quest_template, icon_offset=icon_offset)
