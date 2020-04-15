from src.UI.Button import Button


class BeeSocket(Button):
    def __init__(self, parent, path_to_image: str, position: (int, int), is_active=True) -> None:
        Button.__init__(self, parent=parent, path_to_image=path_to_image, position=position)
        self.is_active = is_active
        self.bee = None

    def on_click(self) -> None:
        print("Select bee")
