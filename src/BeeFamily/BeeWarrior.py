from src.BeeFamily.Bee import Bee
from src.BeeFamily.Bonuses.IBonus import IBonus, RandomResourceBonus, IncreaseResourcesBonus, SpeedUpBonus, HealthBonus


class BeeWarrior(Bee):
    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1, bonus: IBonus = None) -> None:
        if not bonus:
            bonus = IBonus.get_random_bonus([RandomResourceBonus(), IncreaseResourcesBonus(),
                                             SpeedUpBonus(), HealthBonus()])
        Bee.__init__(self, parent=parent, position=position, level=level, bonus=bonus)
        self.set_image("/bee/bee2.png")
        self._dna_code = "B"
