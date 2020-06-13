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

    def lock(self) -> None:
        super().lock()
        self.text_label.change_color((82, 82, 82))

    def unlock(self) -> None:
        super().unlock()
        self.text_label.change_color(self.text_label.normal_color)

    def show(self) -> None:
        super().show()
        self.text_label.show()

    def hide(self) -> None:
        super().hide()
        self.text_label.hide()

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
