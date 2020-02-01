from abc import ABC, abstractmethod


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
        return self.current_xp

    @current_xp.setter
    def current_xp(self, value) -> None:
        if not self.xp_enabled:
            return
        if self.current_xp > self.max_xp:
            over_xp = self.current_xp = self.max_xp
            self.changeLevelTo(self.current_level+1)
            self.current_xp += over_xp
        elif self.current_xp == self.max_xp:
            self.changeLevelTo(self.current_level+1)

    @property
    def current_level(self) -> int:
        return self.__current_level

    def changeLevelTo(self, level: int) -> bool:
        if level < 0 or level > self.max_level:
            return False

        self.__current_level = level
        if level == self.max_level:
            self.xp_enabled = False
            self.current_xp = 0
            self.max_xp = 0
        return True
