from src.Interfaces.Levelable import Levelable


class Bee(Levelable):
    def __init__(self, level=1) -> None:
        Levelable.__init__(self)
        self.max_xp = 100
        self.speed = 0
        self.__current_hp = 0
        self.__max_hp = 0
        self.min_hp = 0
        self.need_hive_level = 0
        self.name = Bee.getRandomName()
        self.change_level_to(level)

    @staticmethod
    def getRandomName() -> str:
        return "RandomName"

    @property
    def max_hp(self) -> int:
        return self.__max_hp

    @property
    def current_hp(self) -> int:
        return self.__current_hp

    @current_hp.setter
    def current_hp(self, value) -> None:
        if value < self.min_hp:
            self.__current_hp = self.min_hp
        elif value >= self.max_hp:
            self.__current_hp = self.max_hp
        else:
            self.__current_hp = value

    def change_level_to(self, level: int) -> bool:
        if not super().change_level_to(level):
            return False

        if level == 1:
            self.speed = 5
            self.__max_hp = 70
            self.max_xp = 100
            self.need_hive_level = 1
        elif level == 2:
            self.speed = 10
            self.__max_hp = 100
            self.max_xp = 150
        elif level == 3:
            self.speed += 2
            self.__max_hp = 120
            self.max_xp = 200
            self.need_hive_level = 2

        self.current_hp = self.max_hp
        # print("Speed: {}".format(self.speed))
        # print("Hp: {0}/{1}".format(self.current_hp, self.max_hp))
        # print("Xp: {0}/{1}".format(self.current_xp, self.max_xp))
        # print("Xp enabled: {}".format(self.xp_enabled))
        # print("---")
        return True
