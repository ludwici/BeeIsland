from src.UI.Button import Button, ButtonState, ButtonEventType


class RadioButton(Button):
    __slots__ = ("group")

    def __init__(self, parent, group, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path, position=position, state=state)
        self.group = group
        self.group.add_button(self)
        self.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.select()})

    def select(self) -> None:
        self.group.unselect_all()
        super().select()
        self.group.current_button = self
