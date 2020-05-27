from abc import ABC, abstractmethod

from Quests.Questable import Questable


class IBonus(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def setup_bonus(self, q: Questable) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class TimeBonus(IBonus):
    __slots__ = "__time"

    def __init__(self, time_val) -> None:
        IBonus.__init__(self)
        self.__time = time_val

    def setup_bonus(self, q: Questable) -> None:
        q.time += self.__time

    def __str__(self) -> str:
        return "+{0} к времени".format(self.__time)


class ScoreBonus(IBonus):
    __slots__ = "__score"

    def __init__(self, score_val) -> None:
        IBonus.__init__(self)
        self.__score = score_val

    def setup_bonus(self, q: Questable) -> None:
        q.score_modifier_percent += self.__score

    def __str__(self) -> str:
        return "+{0}% к общему счёту".format(self.__score)
