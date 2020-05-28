import random
from enum import Enum

import pygame

from src.Database.Localization import Localization
from src.Interfaces.Drawable import Drawable
from src.Interfaces.Levelable import Levelable
from src.Quests.Questable import Questable


class Bee(Levelable, Drawable):
    __slots__ = ("speed", "__current_hp", "__max_hp", "need_hive_level", "name", "_image", "__current_level",
                 "__max_level", "xp_enabled", "__current_xp", "max_xp", "_bonus", "_localization", "__sex")

    class BeeSex(Enum):
        MALE = 1,
        FEMALE = 2

    def __init__(self, parent, bonus, position: (int, int) = (0, 0), level: int = 1) -> None:
        Levelable.__init__(self)
        Drawable.__init__(self, parent=parent, position=position)
        self._localization = Localization("Bee")
        self.max_xp = 100
        self.speed = 0
        self.__sex = random.choice([Bee.BeeSex.MALE, Bee.BeeSex.FEMALE])
        self.__current_hp = 0
        self.__max_hp = 0
        self.min_hp = 0
        self.need_hive_level = 0
        self.name = self.get_random_name()
        self.change_level_to(level)
        self._image = None
        self._bonus = bonus
        self.set_locale_to_bonus()

    def draw(self, screen: pygame.Surface) -> None:
        if self._image:
            screen.blit(self._image, self._rect)

    def set_locale_to_bonus(self):
        if isinstance(self._bonus.__slots__, tuple):
            name = self._bonus.__slots__[0]
        else:
            name = self._bonus.__slots__
        d = self._localization.get_params_by_string("bonuses")[name.lstrip("_")]
        self._bonus.set_description(d)

    def set_image(self, path: str) -> None:
        self._image = pygame.image.load(path)
        self._rect.width = self._image.get_rect().width
        self._rect.height = self._image.get_rect().height

    def setup_bonus(self, q: Questable):
        self._bonus.setup_bonus(q)

    def remove_bonus(self, q: Questable):
        self._bonus.remove_bonus(q)

    def get_random_name(self) -> str:
        prefix = "m" if self.__sex is Bee.BeeSex.MALE else "f"
        names = self._localization.get_params_by_string("{0}_names".format(prefix))
        result = random.choice(names)
        return result

    @property
    def bonus(self) -> str:
        return str(self._bonus)

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
        return True
