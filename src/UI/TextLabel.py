import pygame

from src.Interfaces.RenderObject import RenderObject
from src.Utils import resource_path


class TextLabel(RenderObject):
    __slots__ = ("_font_name", "_font_size", "_bold", "_font", "_text", "_color", "_image")

    def __init__(self, parent, font_size: int, text: str = "", font_name: str = "segoeprint",
                 position: (int, int) = (0, 0),
                 bold: bool = False, color: tuple = (159, 80, 17)) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        self._font_name = font_name
        self._font_size = font_size
        self._bold = bold
        self._font = pygame.font.Font(resource_path("res/fonts/{0}.ttf".format(self._font_name)), self._font_size)
        self._font.set_bold(self._bold)
        self._text = text
        self._color = color
        self._image = None
        self.set_text(text)

    def set_text(self, text: str) -> None:
        self._text = text
        self._image = self._font.render(self._text, True, self._color)
        self._rect.w, self._rect.h = self._image.get_rect().w, self._image.get_rect().h

    def draw(self, screen: pygame.Surface) -> None:
        if not self._text:
            return
        screen.blit(self._image, self._rect)
