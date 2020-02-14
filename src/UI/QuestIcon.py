from src.UI.Button import Button


class QuestIcon(Button):
    def __init__(self, parent, path_to_image: str, position: (int, int)) -> None:
        Button.__init__(self, parent=parent, path_to_image=path_to_image, position=position)

    def update(self, dt) -> None:
        pass
