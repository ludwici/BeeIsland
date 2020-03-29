import pygame

from src.Interfaces.Drawable import Drawable


class TextLabel(Drawable):
    def __init__(self, parent, text: str, position: (int, int), font_name: str, font_size: int, bold: bool = False,
                 color: tuple = (255, 255, 255)) -> None:
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
        self._text = text
        self._image = self._font.render(self._text, True, self._color)
        self._rect = self._image.get_rect()

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._image, self._rect)
