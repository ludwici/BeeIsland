from collections import deque
from typing import Tuple, Any

import pygame
from pygame.rect import Rect

from src.UI.TextLabel import TextLabel


class MultilineTextLabel(TextLabel):
    __slots__ = ("__rendered_text", "line_length", "line_spacing")

    def __init__(self, parent, position: (int, int), font_size: int, line_length: int, bold=False,
                 color: tuple = (159, 80, 17), font_name: str = "segoeprint", text: str = "") -> None:
        self.__rendered_text = []
        self.line_length = line_length
        self.line_spacing = 2
        TextLabel.__init__(self, parent=parent, text=text, position=position, font_name=font_name, font_size=font_size,
                           color=color, bold=bold)

    @property
    def line_count(self) -> int:
        return len(self.__rendered_text)

    def __render_font(self, font, msg, color, msg_center) -> Tuple[Any, Rect]:
        msg = font.render(msg, 1, color)
        rect = msg.get_rect(topleft=msg_center)
        return msg, rect

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self.set_text(self._text)

    def __add_new_line(self, text: str):
        msg_center = (self.position[0], self.position[1] + self.line_count * (self._font_size + self.line_spacing))
        msg_data = self.__render_font(self._font, text, self._color, msg_center)
        self.__rendered_text.append(msg_data)

    def set_text(self, text) -> None:
        if not text:
            return
        self._text = text
        self.__rendered_text.clear()
        tmp = deque(self._text.split())
        str_tmp = ""
        size = 0
        i = 0
        while tmp:
            t = tmp.popleft()
            size += self._font.size(t)[0]
            if size >= self.line_length:
                size = self._font.size(t)[0]
                self.__add_new_line(str_tmp)
                str_tmp = t + " "
            else:
                str_tmp += t + " "

        self.__add_new_line(str_tmp)
        w = max([r[1].width for r in self.__rendered_text])
        h = self.line_count * (self._font_size + self.line_spacing)
        self._rect.w, self._rect.h = w, h

    def draw(self, screen: pygame.Surface) -> None:
        [screen.blit(*msg) for msg in self.__rendered_text]
