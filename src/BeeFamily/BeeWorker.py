from src.BeeFamily.Bee import Bee
from src.BeeFamily.Bonuses.IBonus import IBonus


class BeeWorker(Bee):
    __slots__ = "_can_hard"

    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1, bonus: IBonus = None) -> None:
        Bee.__init__(self, parent=parent, position=position, level=level, bonus=bonus)
        self.set_image("../res/images/bee/bee1.png")
        self._can_hard = False

    @property
    def can_hard(self) -> bool:
        return self._can_hard
