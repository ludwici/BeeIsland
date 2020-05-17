from src.BeeFamily.Bee import Bee


class BeeQueen(Bee):
    def __init__(self, parent, position: (int, int), level: int = 1) -> None:
        Bee.__init__(self, parent=parent, position=position, level=level)
