from src.UI.Button import Button


class BeeSocket(Button):
    def __init__(self, parent, path_to_image: str, position: (int, int)) -> None:
        Button.__init__(self, parent=parent, path_to_image=path_to_image, position=position)
        self.bee = None

    def on_click(self) -> None:
        print("Select bee")
