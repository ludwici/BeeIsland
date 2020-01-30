from src.Bee import Bee
from src.Interfaces import Levelable


class BeeHive(Levelable):
    def __init__(self):
        Levelable.__init__(self)
        self.max_xp = 5
        self.max_size = 0
        self.__bee_list = []

    def changeLevelTo(self, level: int) -> bool:
        if not super().changeLevelTo(level):
            return False

        if level == 1:
            self.max_size = 5
            self.max_xp = 5
        elif level == 2:
            self.max_size += 2
            self.max_xp = 10

        return True

    @property
    def size(self):
        return len(self.__bee_list)

    @property
    def bee_list(self):
        return self.__bee_list

    def addBee(self, bee: Bee):
        if self.size >= self.max_size:
            return

        if bee.need_hive_level > self.current_level:
            return

        self.__bee_list.append(bee)
