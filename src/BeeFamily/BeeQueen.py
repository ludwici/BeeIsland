from src.BeeFamily.Bee import Bee


class BeeQueen(Bee):
    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1) -> None:
        Bee.__init__(self, parent=parent, position=position, level=level, bonus=None)
        self.set_image("/bee/queen1.png")
