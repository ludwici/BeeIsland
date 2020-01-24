from src.Interfaces import Levelable


class Bee(Levelable):
    def __init__(self, level=1):
        Levelable.__init__(self)
        self.max_xp = 100
        self.speed = 0
        self.__current_hp = 0
        self.__max_hp = 0
        self.min_hp = 0
        self.need_hive_level = 0
        self.name = Bee.getRandomName()
        self.changeLevelTo(level)

    @staticmethod
    def getRandomName() -> str:
        return "RandomName"

    @property
    def max_hp(self):
        return self.__max_hp

    @property
    def current_hp(self):
        return self.__current_hp

    @current_hp.setter
    def current_hp(self, value):
        if value < self.min_hp:
            self.current_hp = self.min_hp
        elif value >= self.max_hp:
            self.current_hp = self.max_hp
        else:
            self.current_hp = value

    def changeLevelTo(self, level: int) -> bool:
        if not super().changeLevelTo(level):
            return False

        if level == 1:
            self.speed = 10
            self.__max_hp = 100
            self.max_xp = 100
            self.need_hive_level = 1
        elif level == 2:
            self.speed += 2
            self.__max_hp = 120
            self.max_xp = 200

        self.current_hp = self.max_hp
        return False
