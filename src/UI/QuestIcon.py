from src.UI.Button import Button, ButtonState


class QuestIcon(Button):
    def __init__(self, parent, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path, position=position, state=state)

    def on_click(self) -> None:
        self.parent.show_popup()
