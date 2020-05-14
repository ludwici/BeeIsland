from src.UI.Button import ButtonState
from src.UI.RadioButton import RadioButton


class BeeSocket(RadioButton):
    def __init__(self, parent, group, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        RadioButton.__init__(self, parent=parent, group=group, normal_image_path=normal_image_path,
                             position=position, state=state)
        self.bee = None
