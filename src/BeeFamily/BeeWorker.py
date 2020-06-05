from src.BeeFamily.Bee import Bee
from src.BeeFamily.Bonuses.IBonus import IBonus, ScoreBonus, TimeBonus


class BeeWorker(Bee):
    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1, bonus: IBonus = None) -> None:
        if not bonus:
            bonus = IBonus.get_random_bonus([TimeBonus(), ScoreBonus()])
        Bee.__init__(self, parent=parent, position=position, level=level, bonus=bonus)
        self.set_image("/bee/bee1.png")
