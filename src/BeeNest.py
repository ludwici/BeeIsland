from src.Bee import Bee
from src.Interfaces import Levelable


class BeeNest(Levelable):
    def __init__(self, level=0) -> None:
        Levelable.__init__(self)
        self.__bee_list = []
        self.__current_level = level
        self.__max_level = 1
        self.max_size = 0
        self.changeLevelTo(level)

    def changeLevelTo(self, level: int) -> bool:
        if not super().changeLevelTo(level):
            return False

        if level == 0:
            self.max_size = 3
            self.max_xp = 3
        elif level == 1:
            self.max_size += 2
            self.max_xp = 5
        elif level == 2:
            self.max_size += 2
            self.max_xp = 10

        return True

    @property
    def size(self) -> int:
        return len(self.__bee_list)

    @property
    def bee_list(self) -> list:
        return self.__bee_list

    def addBee(self, bee: Bee) -> bool:
        if self.size >= self.max_size:
            return False

        if bee.need_hive_level > self.current_level:
            return False

        self.__bee_list.append(bee)
        return True
