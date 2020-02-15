from abc import ABC


class Levelable(ABC):
    def __init__(self) -> None:
        self.__current_level = 0
        self.__max_level = 10
        self.xp_enabled = True
        self.__current_xp = 0
        self.max_xp = 0

    @property
    def max_level(self) -> int:
        return self.__max_level

    @property
    def current_xp(self) -> int:
        return self.__current_xp

    def give_xp(self, value: int) -> None:
        if not self.xp_enabled:
            return
        if (self.current_xp + value) >= self.max_xp:
            over_xp = self.current_xp + value - self.max_xp
            self.change_level_to(self.current_level + 1)
            value = over_xp
        self.__current_xp = value
        # print("Xp: {0}/{1}".format(self.current_xp, self.max_xp))

    @property
    def current_level(self) -> int:
        return self.__current_level

    def change_level_to(self, level: int) -> bool:
        if level < 0 or level > self.max_level:
            return False

        self.__current_level = level
        self.__current_xp = 0
        if level == self.max_level:
            self.xp_enabled = False
            self.max_xp = 0
        return True
