from src import MapZone
from src.Interfaces.Questable import Questable


class Match3(Questable):
    def __init__(self, zone: MapZone, icon_position: (int, int)) -> None:
        Questable.__init__(self, zone=zone, icon_position=icon_position)
        self.icon_btn.add_action(lambda: self.zone.parent.main_window.change_scene("Match3"))
