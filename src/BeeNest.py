from copy import copy

from src.BeeFamily.Bee import Bee
from src.Interfaces.Levelable import Levelable


class BeeNest(Levelable):
    __slots__ = ("__current_level", "__max_level", "xp_enabled", "__current_xp", "max_xp", "__bee_list")

    def __init__(self, level=1) -> None:
        Levelable.__init__(self)
        self.__bee_list = []
        self.__max_level = 1
        self.__max_size = 0
        self.change_level_to(level)

    def change_level_to(self, level: int) -> bool:
        if not super().change_level_to(level):
            return False

        if level == 1:
            self.__max_size = 3
            self.max_xp = 3
        elif level == 2:
            self.__max_size += 1
            self.max_xp = 5
        elif level == 3:
            self.__max_size += 1
            self.max_xp = 10

        return True

    @property
    def max_size(self):
        return copy(self.__max_size)

    @property
    def size(self) -> int:
        return len(self.__bee_list)

    @property
    def bee_list(self) -> list:
        return copy(self.__bee_list)

    def add_bee(self, bee: Bee) -> bool:
        if self.size > self.__max_size:
            return False

        if bee.need_hive_level > self.current_level:
            return False

        self.__bee_list.append(bee)
        return True
