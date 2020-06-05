import math
import random
from enum import Enum

import pygame

from src.Database.Localization import Localization
from src.Interfaces.Drawable import Drawable
from src.Interfaces.Levelable import Levelable
from src.Quests.Quest import Quest


class Bee(Levelable, Drawable):
    __slots__ = ("__base_speed", "speed_mod", "hp_mod", "__current_hp", "__max_hp", "need_hive_level", "name", "_image",
                 "__current_level",
                 "__max_level", "xp_enabled", "__current_xp", "max_xp", "bonus", "_localization", "__sex", "socket_id")

    class BeeSex(Enum):
        MALE = 1,
        FEMALE = 2

    def __init__(self, parent, bonus, position: (int, int) = (0, 0), level: int = 1, sex: BeeSex = None) -> None:
        Levelable.__init__(self)
        Drawable.__init__(self, parent=parent, position=position)
        self._localization = Localization("Bee")
        self.max_xp = 100
        self.__base_speed = 0
        self.speed_mod = 0
        self.hp_mod = 0
        self.__sex = sex if sex else random.choice([Bee.BeeSex.MALE, Bee.BeeSex.FEMALE])
        self.__current_hp = 0
        self.__max_hp = 0
        self.__min_hp = 0
        self.need_hive_level = 0
        prefix = self.get_prefix()
        self.name = self.get_random_name(prefix)
        self.change_level_to(level)
        self._image = None
        self.bonus = bonus
        self.socket_id = -1
        self.current_hp = self.max_hp
        self.set_locale_to_bonus()

    def get_prefix(self) -> str:
        return "m" if self.__sex is Bee.BeeSex.MALE else "f"

    def upgrade_name(self, mod: str) -> None:
        prefix = self.get_prefix()
        upgrades = self._localization.get_params_by_string("{0}_prefixes".format(prefix))[mod]
        self.name = "{0} {1}".format(random.choice(upgrades), self.name)

    def draw(self, screen: pygame.Surface) -> None:
        if self._image:
            screen.blit(self._image, self._rect)

    def set_locale_to_bonus(self):
        if not self.bonus:
            return
        if isinstance(self.bonus.__slots__, tuple):
            name = self.bonus.__slots__[0]
        else:
            name = self.bonus.__slots__
        d = self._localization.get_params_by_string("bonuses")[name.lstrip("_")]
        self.bonus.set_description(d)

    def set_image(self, path: str) -> None:
        self._image = pygame.image.load("{0}{1}".format(self._res_dir, path))
        self._rect.width = self._image.get_rect().width
        self._rect.height = self._image.get_rect().height

    def setup_bonus(self, q: Quest):
        self.bonus.setup_bonus(q)

    def remove_bonus(self, q: Quest):
        self.bonus.remove_bonus(q)

    def get_random_name(self, prefix) -> str:
        names = self._localization.get_params_by_string("{0}_names".format(prefix))
        result = random.choice(names)
        return result

    def modify_bonus(self):
        self.bonus.modify()
        self.set_locale_to_bonus()

    # @property
    # def bonus(self) -> IBonus:
    #     return self._bonus

    @property
    def max_hp(self) -> int:
        return self.__max_hp + self.hp_mod

    @max_hp.deleter
    def max_hp(self) -> None:
        del self.hp_mod
        del self.__max_hp

    @property
    def current_hp(self) -> int:
        return self.__current_hp

    @current_hp.setter
    def current_hp(self, value) -> None:
        if value < self.__min_hp:
            self.__current_hp = self.__min_hp
        elif value >= self.max_hp:
            self.__current_hp = self.max_hp
        else:
            self.__current_hp = value

    @current_hp.deleter
    def current_hp(self) -> None:
        del self.__current_hp

    @property
    def speed(self) -> float:
        return self.__base_speed + self.speed_mod

    @speed.deleter
    def speed(self) -> None:
        del self.speed_mod
        del self.__base_speed

    def change_level_to(self, level: int) -> bool:
        if not super().change_level_to(level):
            return False

        if level == 1:
            self.__base_speed = 3
            self.__max_hp = 70
            self.need_hive_level = 1
        elif level == 2:
            self.__base_speed = 4
            self.__max_hp = 92
        elif level == 3:
            self.__max_hp = 100
            self.need_hive_level = 2
        elif level == 4:
            self.__max_hp = 150
        elif level == 5:
            self.__max_hp = 180
            self.__base_speed = 5

        self.max_xp = math.ceil(math.exp(level) * 100)

        return True
