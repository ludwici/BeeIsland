from BeeNest import BeeNest
from InGameResources.ResourceBag import ResourceBag
from src.BeeFamily.BeeWorker import BeeWorker
from src.Farm import Farm


class Player:
    def __init__(self) -> None:
        self.name = "Player"
        self.resources = ResourceBag()
        self.farm = Farm()
        for i in range(3):
            self.farm.add_out_of_hive_bee(BeeWorker(parent=self))

    def already_has_hive(self, hive: BeeNest):
        return hive in self.farm.hive_list

    @property
    def can_buy_new_hive(self) -> bool:
        return len(self.farm.hive_list) < self.farm.max_active_hive_count
