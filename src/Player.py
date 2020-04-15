from src.Farm import Farm
from src.ResourceBag import ResourceBag


class Player:
    def __init__(self) -> None:
        self.name = "Player"
        self.resources = ResourceBag()
        self.farm = Farm()

    @property
    def can_buy_new_hive(self) -> bool:
        return len(self.farm.hive_list) < self.farm.max_active_hive_count

