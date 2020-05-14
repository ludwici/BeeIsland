import pygame

from src.UI import TextLabel
from src.UI.Button import Button


class TextButton(Button):
    def __init__(self, parent, normal_image_path, position: (int, int) = (0, 0),
                 text_label: TextLabel = None, text_padding: (int, int) = (0, 0)) -> None:
        self.text_label = text_label
        self.padding = text_padding
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path, position=position)
        # self.set_position(position)

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self.text_label.set_position((self.position[0] + self.padding[0], self.position[1] + self.padding[1]))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.text_label.draw(screen)
