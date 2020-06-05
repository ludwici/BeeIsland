import random
from abc import ABC, abstractmethod

from src.Database.Database import Database
from src.InGameResources.ResourceBag import ResourceBag
from src.Quests.Quest import Quest


class IBonus(ABC):
    __slots__ = "_description"

    def __init__(self) -> None:
        pass

    @abstractmethod
    def setup_bonus(self, q: Quest) -> None:
        pass

    @abstractmethod
    def remove_bonus(self, q: Quest) -> None:
        pass

    def set_description(self, description: str) -> None:
        self._description = description

    @property
    def description(self) -> str:
        return self._description

    @abstractmethod
    def modify(self) -> None:
        pass

    @staticmethod
    def get_random_bonus(bonus_seq: list = None):
        return random.choice(bonus_seq)


class TimeBonus(IBonus):
    __slots__ = "__time"

    def __init__(self, time_val=10) -> None:
        IBonus.__init__(self)
        self.__time = time_val

    def setup_bonus(self, q: Quest) -> None:
        q.time += self.__time

    def remove_bonus(self, q: Quest) -> None:
        q.time -= self.__time

    def set_description(self, description: str) -> None:
        self._description = description.format(self.__time)

    def modify(self) -> None:
        self.__time += 2


class ScoreBonus(IBonus):
    __slots__ = "__score"

    def __init__(self, score_val=10) -> None:
        IBonus.__init__(self)
        self.__score = score_val

    def setup_bonus(self, q: Quest) -> None:
        q.score_modifier_percent += self.__score

    def remove_bonus(self, q: Quest) -> None:
        q.score_modifier_percent -= self.__score

    def set_description(self, description: str) -> None:
        self._description = description.format(self.__score)

    def modify(self) -> None:
        self.__score += 5


class RandomResourceBonus(IBonus):
    __slots__ = ("resource", "__items_ids")

    def __init__(self, items_ids: list = None):
        IBonus.__init__(self)
        if not items_ids:
            self.__items_ids = [1, 2, 3, 4, 5]
        else:
            self.__items_ids = items_ids
        self.resource = ResourceBag()
        self.resource.append(self.__get_random_resource())

    def __get_random_resource(self):
        db = Database.get_instance()
        r_id = random.choice(self.__items_ids)
        resource = db.get_resource_by_id(r_id)
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
        resource.value = value
        return resource

    def setup_bonus(self, q: Quest) -> None:
        q.additional_rewards.append(self.resource)

    def remove_bonus(self, q: Quest) -> None:
        q.additional_rewards.remove(self.resource)

    def modify(self) -> None:
        self.resource.append(self.__get_random_resource())


class IncreaseResourcesBonus(IBonus):
    __slots__ = "__percent"

    def __init__(self, percent=10) -> None:
        IBonus.__init__(self)
        self.__percent = percent

    def setup_bonus(self, q: Quest) -> None:
        q.resources_modifier += self.__percent

    def remove_bonus(self, q: Quest) -> None:
        q.resources_modifier -= self.__percent

    def modify(self) -> None:
        self.__percent += 2


class SpeedUpBonus(IBonus):
    __slots__ = "__speed"

    def __init__(self, speed=0.5) -> None:
        IBonus.__init__(self)
        self.__speed = speed

    def setup_bonus(self, q: Quest) -> None:
        for b in q.bee_list:
            b.speed_mod += self.__speed

    def remove_bonus(self, q: Quest) -> None:
        for b in q.bee_list:
            b.speed_mod -= self.__speed

    def modify(self) -> None:
        self.__speed += 0.2


class HealthBonus(IBonus):
    __slots__ = "__health"

    def __init__(self, health=10):
        IBonus.__init__(self)
        self.__health = health

    def setup_bonus(self, q: Quest) -> None:
        for b in q.bee_list:
            b.current_hp += self.__health

    def remove_bonus(self, q: Quest) -> None:
        for b in q.bee_list:
            b.current_hp -= self.__health

    def set_description(self, description: str) -> None:
        self._description = description.format(self.__health)

    def modify(self) -> None:
        self.__health += 2
