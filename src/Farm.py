from copy import copy

from src.BeeFamily.Bee import Bee
from src.BeeNest import BeeNest


class Farm:
    def __init__(self) -> None:
        self.__hive_list = []
        self.__out_of_hive_bee_list = []
        self.max_active_hive_count = 1
        self.max_hive_slots = 6
        self.max_hive_level = 5

    @property
    def active_hives_count(self) -> int:
        return len(self.hive_list)

    @property
    def hive_list(self) -> list:
        return copy(self.__hive_list)

    @property
    def out_of_hive_bee_list(self) -> list:
        return copy(self.__out_of_hive_bee_list)

    def add_out_of_hive_bee(self, b: Bee) -> None:
        self.__out_of_hive_bee_list.append(b)

    def add_hive(self, hive: BeeNest) -> bool:
        if self.active_hives_count > self.max_active_hive_count:
            return False

        if hive.current_level > self.max_hive_level:
            return False

        self.__hive_list.append(hive)
        return True
