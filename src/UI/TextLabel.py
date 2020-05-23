import pygame

from src.Interfaces.Drawable import Drawable


class TextLabel(Drawable):
    def __init__(self, parent, font_name: str, font_size: int, text: str = "", position: (int, int) = (0, 0),
                 bold: bool = False, color: tuple = (255, 255, 255)) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self._font_name = font_name
        self._font_size = font_size
        self._bold = bold
        self._font = pygame.font.SysFont(self._font_name, self._font_size, self._bold)
        self._text = text
        self._color = color
        self._image = None
        self.set_text(text)

    def set_text(self, text: str) -> None:
        if not text:
            return
        self._text = text
        self._image = self._font.render(self._text, True, self._color)
        self._rect.w, self._rect.h = self._image.get_rect().w, self._image.get_rect().h

    def draw(self, screen: pygame.Surface) -> None:
        if not self._text:
            return
        screen.blit(self._image, self._rect)
