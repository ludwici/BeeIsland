import pygame

from src.UI import TextLabel
from src.UI.Button import Button


class TextButton(Button):
    __slots__ = ("text_label", "padding")

    def __init__(self, parent, normal_image_path, position: (int, int) = (0, 0),
                 text_label: TextLabel = None, text_padding: (int, int) = (0, 0)) -> None:
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path, position=position)
        self.text_label = text_label
        self.padding = text_padding

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self.text_label.set_position((self.position[0] + self.padding[0], self.position[1] + self.padding[1]))

    def set_padding(self, padding: (int, int)) -> None:
        self.padding = padding
        self.set_position(self.position)

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.text_label.draw(screen)

    def set_text(self, text: str) -> None:
        self.text_label.set_text(text)
