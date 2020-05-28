import random
from abc import ABC, abstractmethod

from src.Database.Database import Database
from src.Quests.Questable import Questable


class IBonus(ABC):
    __slots__ = "_description"

    def __init__(self) -> None:
        pass

    @abstractmethod
    def setup_bonus(self, q: Questable) -> None:
        pass

    @abstractmethod
    def remove_bonus(self, q: Questable) -> None:
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        pass

    def __str__(self) -> str:
        return self._description


class TimeBonus(IBonus):
    __slots__ = "__time"

    def __init__(self, time_val) -> None:
        IBonus.__init__(self)
        self.__time = time_val

    def setup_bonus(self, q: Questable) -> None:
        q.time += self.__time

    def remove_bonus(self, q: Questable) -> None:
        q.time -= self.__time

    def set_description(self, description: str) -> None:
        self._description = description.format(self.__time)


class ScoreBonus(IBonus):
    __slots__ = "__score"

    def __init__(self, score_val) -> None:
        IBonus.__init__(self)
        self.__score = score_val

    def setup_bonus(self, q: Questable) -> None:
        q.score_modifier_percent += self.__score

    def remove_bonus(self, q: Questable) -> None:
        q.score_modifier_percent -= self.__score

    def set_description(self, description: str) -> None:
        self._description = description.format(self.__score)


class RandomResourceBonus(IBonus):
    __slots__ = ("resource", "__items_ids")

    def __init__(self, items_ids: list):
        IBonus.__init__(self)
        self.__items_ids = items_ids
        db = Database.get_instance()
        r_id = random.choice(self.__items_ids)
        self.resource = db.get_resource_by_id(r_id)
        value = 0
        if r_id == 1:
            value = random.randint(5, 10)
        elif r_id == 2:
            value = random.randint(2, 6)
        elif r_id == 3:
            value = random.randint(1, 10)
        elif r_id == 4:
            value = random.randint(1, 5)
        elif r_id == 5:
            value = random.randint(1, 3)
        self.resource.value = value

    def setup_bonus(self, q: Questable) -> None:
        q.additional_rewards.append(self.resource)

    def remove_bonus(self, q: Questable) -> None:
        q.additional_rewards.remove(self.resource)

    def set_description(self, description: str) -> None:
        self._description = description
