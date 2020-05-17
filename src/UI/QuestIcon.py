from src.UI.Button import Button, ButtonState, ButtonEventType


class QuestIcon(Button):
    def __init__(self, parent, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path, position=position, state=state)
        self.show_popup()

    @Button.register_event(ButtonEventType.ON_CLICK_LB)
    def show_popup(self):
        self.parent.show_popup()
