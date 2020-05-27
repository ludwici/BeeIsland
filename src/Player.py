from BeeFamily.Bonuses.IBonus import TimeBonus, ScoreBonus
from BeeNest import BeeNest
from InGameResources.ResourceBag import ResourceBag
from src.BeeFamily.BeeWorker import BeeWorker
from src.Farm import Farm


class Player:
    __slots__ = ("name", "resources", "farm")

    def __init__(self) -> None:
        self.name = "Player"
        self.resources = ResourceBag()
        self.farm = Farm()
        self.farm.add_out_of_hive_bee(BeeWorker(parent=self, bonus=TimeBonus(time_val=10)))
        self.farm.add_out_of_hive_bee(BeeWorker(parent=self, bonus=ScoreBonus(score_val=10)))
        self.farm.add_out_of_hive_bee(BeeWorker(parent=self))

    def already_has_hive(self, hive: BeeNest):
        return hive in self.farm.hive_list

    @property
    def can_buy_new_hive(self) -> bool:
        return len(self.farm.hive_list) < self.farm.max_active_hive_count
