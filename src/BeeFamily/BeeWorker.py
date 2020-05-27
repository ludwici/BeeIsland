from BeeFamily.Bonuses.IBonus import IBonus
from Quests.Questable import Questable
from src.BeeFamily.Bee import Bee


class BeeWorker(Bee):
    __slots__ = ("_can_hard", "_bonus")

    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1, bonus: IBonus = None) -> None:
        Bee.__init__(self, parent=parent, position=position, level=level)
        self.set_image("../res/images/bee/bee1.png")
        self._can_hard = False
        self._bonus = bonus

    @property
    def can_hard(self) -> bool:
        return self._can_hard

    @property
    def bonus(self) -> str:
        return str(self._bonus)

    def setup_bonus(self, q: Questable):
        self._bonus.setup_bonus(q)
