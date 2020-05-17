from src.BeeFamily.Bee import Bee


class BeeWorker(Bee):
    def __init__(self, parent, position: (int, int) = (0, 0), level: int = 1) -> None:
        Bee.__init__(self, parent=parent, position=position, level=level)
        self.set_image("../res/images/bee/bee1.png")
