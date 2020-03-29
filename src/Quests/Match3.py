from src.Interfaces.Questable import Questable, QuestDifficult


class Match3(Questable):
    def __init__(self, icon_position: (int, int), difficult: QuestDifficult, quest_title: str = "Три в ряд") -> None:
        Questable.__init__(self, icon_position=icon_position, difficult=difficult, quest_title=quest_title)
