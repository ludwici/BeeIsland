import math
import random
from enum import Enum

import pygame

from Interfaces.GeneCode import GeneCode
from src.Database.Localization import Localization
from src.Interfaces.RenderObject import RenderObject
from src.Quests.Quest import Quest


class Bee(RenderObject, GeneCode):
    __slots__ = ("_base_speed", "speed_mod", "hp_mod", "__current_hp", "name", "_image", "_max_hp", "__max_level",
                 "xp_enabled", "__current_xp", "max_xp", "bonus", "_localization", "__sex", "socket_id", "_dna_code",
                 "generation")

    class BeeSex(Enum):
        MALE = 1,
        FEMALE = 2

    def __init__(self, parent, bonus, position: (int, int) = (0, 0), level: int = 1, sex: BeeSex = None) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        GeneCode.__init__(self)
        self._localization = Localization("Bee")
        self.max_xp = 100
        self.generation = 1
        self.__sex = sex if sex else random.choice([Bee.BeeSex.MALE, Bee.BeeSex.FEMALE])
        self.__current_hp = 0
        self.__max_level = 5
        self.__current_xp = 1
        self.xp_enabled = True
        prefix = self.get_prefix()
        self.name = self.get_random_name(prefix)
        self.change_level_to(level)
        self._image = None
        self.bonus = bonus
        self.socket_id = -1
        self.current_hp = self.max_hp
        self.set_locale_to_bonus()

    @property
    def dna_code(self) -> str:
        return self._dna_code

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

    def give_xp(self, value: int) -> None:
        if not self.xp_enabled:
            return
        if (self.current_xp + value) > self.max_xp:
            over_xp = self.current_xp + value - self.max_xp
            self.change_level_to(self.current_level + 1)
            value = over_xp
            self.__current_xp = value
        else:
            self.__current_xp += value

    @property
    def current_xp(self) -> int:
        return self.__current_xp

    @property
    def max_level(self) -> int:
        return self.__max_level

    def change_level_to(self, level: int) -> bool:
        if level < 0 or level > self.max_level:
            return False

        self.current_level = level
        self.__current_xp = 1

        if level == 1:
            self._base_speed = 3
            self._max_hp = 70
        elif level == 2:
            self._base_speed = 4
            self._max_hp = 92
        elif level == 3:
            self._max_hp = 100
        elif level == 4:
            self._max_hp = 150
        elif level == 5:
            self._max_hp = 180
            self._base_speed = 5

        self.max_xp = math.ceil(math.exp(level) * 100)

        if level == self.max_level:
            self.xp_enabled = False
            self.max_xp = 0

        return True
