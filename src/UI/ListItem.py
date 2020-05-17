import pygame

from src.UI.Button import Button


class ListItem(Button):
    def __init__(self, parent, data, normal_image_path: str) -> None:
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path)
        self.data = data

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if self.data:
            self.data.handle_event(event)

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        if self.data:
            self.data.get_rect().center = self._rect.center

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.data:
            self.data.draw(screen)
