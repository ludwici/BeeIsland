from src.BeeFamily.BeeQueen import BeeQueen
from src.BeeFamily.BeeWarrior import BeeWarrior
from src.BeeFamily.BeeWorker import BeeWorker
from src.BeeFamily.Bonuses.IBonus import TimeBonus, ScoreBonus, RandomResourceBonus
from src.BeeNest import BeeNest
from src.Farm import Farm
from src.InGameResources.ResourceBag import ResourceBag


class Player:
    __slots__ = ("name", "resources", "farm")

    def __init__(self) -> None:
        self.name = "Player"
        self.resources = ResourceBag()
        self.farm = Farm()
        self.farm.add_out_of_hive_bee(BeeWorker(parent=self, bonus=TimeBonus(time_val=10)))
        self.farm.add_out_of_hive_bee(BeeWorker(parent=self, bonus=ScoreBonus(score_val=10)))
        self.farm.add_out_of_hive_bee(BeeWarrior(parent=self, bonus=RandomResourceBonus(items_ids=[1, 2, 3, 4, 5])))
        self.farm.add_out_of_hive_bee(BeeQueen(parent=self))

    def already_has_hive(self, hive: BeeNest):
        return hive in self.farm.hive_list

    @property
    def can_buy_new_hive(self) -> bool:
        return len(self.farm.hive_list) < self.farm.max_active_hive_count
