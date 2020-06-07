import math
import random
from abc import ABC


class GeneCode(ABC):
    def __init__(self, code, bonus=None) -> None:
        self.current_level = 1
        self.speed_mod = 0
        self._base_speed = 0
        self._min_hp = 0
        self._max_hp = 65
        self._current_hp = 65
        self.hp_mod = 0
        self.generation = 0
        self._dna_code = code
        self.bonus = bonus
        self.__valid_codes = ["AA", "BB", "AB", "Q3", "A1", "B2", "11", "22", "33", "AJ", "BJ"]

    @staticmethod
    def parse_code(code) -> str:
        return ''.join(sorted(code, reverse=any(char.isdigit() for char in code)))

    def __add__(self, other: "GeneCode"):
        code = GeneCode.parse_code(self.dna_code + other.dna_code)
        if code not in self.__valid_codes:
            return None

        if "3" in code:
            from src.BeeFamily.BeeQueen import BeeQueen
            if code[0] == "Q":
                bee = self if isinstance(self, BeeQueen) else other
                bee.give_xp(1)
            else:
                bee = BeeQueen(parent=self)
            return bee

        if "J" in code:
            self.current_hp += 10
            from src.BeeFamily.Bee import Bee
            return self if issubclass(type(self), Bee) else other

        warrior_mod = 2
        if "B" in code:
            warrior_mod += 4

        warrior_percent = (self.current_level + other.current_level) * warrior_mod

        warrior_change = random.random() * 100
        if warrior_change <= warrior_percent or "2" in code and "1" not in code:
            from src.BeeFamily.BeeWarrior import BeeWarrior
            bee = BeeWarrior(parent=self)
        else:
            from src.BeeFamily.BeeWorker import BeeWorker
            bee = BeeWorker(parent=self)

        bonus_chance = random.random() * 100
        if code in ["AA", "BB", "AB"]:
            if bonus_chance <= 30:
                b1_chance = 75 if self.generation > other.generation else 25
                if b1_chance < random.random() * 100:
                    bee.bonus = self.bonus
                else:
                    bee.bonus = other.bonus
                bee.modify_bonus()
                bee.hp_mod = max(self.hp_mod, other.hp_mod)
                bee.speed_mod = max(self.speed_mod, other.speed_mod)
                mod = "bonus"
            else:
                random_param = random.randint(1, 2)
                if random_param == 1:
                    bee.speed_mod = (self.speed + other.speed) * ((self.current_level + other.current_level) / 2) / 100
                    bee.hp_mod = max(self.hp_mod, other.hp_mod)
                    mod = "speed"
                else:
                    bee.hp_mod = math.ceil((((self.current_hp * 10) / 100) + ((other.current_hp * 10) / 100)) / 2)
                    bee.current_hp = bee.max_hp
                    bee.speed_mod = max(self.speed_mod, other.speed_mod)
                    mod = "health"

            bee.upgrade_name(mod)
            bee.generation = max(self.generation, other.generation) + 1

        return bee

    @property
    def dna_code(self) -> str:
        return self._dna_code

    @property
    def max_hp(self) -> int:
        return self._max_hp + self.hp_mod

    @max_hp.deleter
    def max_hp(self) -> None:
        del self.hp_mod
        del self._max_hp

    @property
    def speed(self) -> float:
        return round(self._base_speed + self.speed_mod, 2)

    @speed.deleter
    def speed(self) -> None:
        del self.speed_mod
        del self._base_speed

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value) -> None:
        if value < self._min_hp:
            self._current_hp = self._min_hp
        elif value >= self.max_hp:
            self._current_hp = self.max_hp
        else:
            self._current_hp = value

    @current_hp.deleter
    def current_hp(self) -> None:
        del self._current_hp
