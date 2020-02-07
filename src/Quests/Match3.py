from src.Interfaces.Questable import Questable


class Match3(Questable):
    def __init__(self, zone, icon_position: (int, int)) -> None:
        Questable.__init__(self, zone=zone, icon_position=icon_position)
