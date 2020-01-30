from src.BeeHive import BeeHive


class Farm:
    def __init__(self):
        self.__hive_list = []
        self.max_active_hive_count = 3
        self.max_hive_slots = 6
        self.max_hive_level = 5

    def size(self):
        return len(self.hive_list)

    @property
    def hive_list(self):
        return self.__hive_list

    def addHive(self, hive: BeeHive):
        if self.size() >= self.max_active_hive_count:
            return

        if hive.current_level > self.max_hive_level:
            return

        self.hive_list.append(hive)
