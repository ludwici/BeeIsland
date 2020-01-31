from src.BeeNest import BeeNest


class Farm:
    def __init__(self) -> None:
        self.__hive_list = []
        self.max_active_hive_count = 3
        self.max_hive_slots = 6
        self.max_hive_level = 5

    def size(self):
        return len(self.hive_list)

    @property
    def hive_list(self):
        return self.__hive_list

    def addHive(self, hive: BeeNest) -> bool:
        if self.size() >= self.max_active_hive_count:
            return False

        if hive.current_level > self.max_hive_level:
            return False

        self.hive_list.append(hive)
        return True