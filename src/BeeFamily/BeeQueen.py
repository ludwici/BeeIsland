from src.BeeFamily.Bee import Bee


class BeeQueen(Bee):
    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1) -> None:
        Bee.__init__(self, parent=parent, position=position, level=level, bonus=None, sex=Bee.BeeSex.FEMALE)
        self.set_image("/bee/queen1.png")
        del self.bonus
        del self.speed
        del self.current_hp
        del self.max_hp
