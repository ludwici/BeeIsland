from collections import deque
from typing import Tuple, Any

import pygame
from pygame.rect import Rect

from src.UI.TextLabel import TextLabel


class MultilineTextLabel(TextLabel):
    def __init__(self, parent, text: str, position: (int, int), font_name: str, font_size: int,
                 color: tuple, line_length: int, bold=False) -> None:
        self.__rendered_text = []
        self.line_length = line_length
        self.line_spacing = 2
        self.__line_count = 0
        TextLabel.__init__(self, parent=parent, text=text, position=position, font_name=font_name, font_size=font_size,
                           color=color, bold=bold)

    def __render_font(self, font, msg, color, msg_center) -> Tuple[Any, Rect]:
        msg = font.render(msg, 1, color)
        rect = msg.get_rect(topleft=msg_center)
        return msg, rect

    def set_text(self, value) -> None:
        if not value:
            return
        self._text = value
        self.__rendered_text.clear()
        tmp = deque(self._text.split())
        str_tmp = ""
        size = 0
        i = 0
        while tmp:
            t = tmp.popleft()
            size += self._font.size(t)[0]
            if not tmp:
                str_tmp += t
            if (size + 35) >= self.line_length or not tmp:
                size = self._font.size(t)[0]
                msg_center = (self.position[0], self.position[1] + i * (self._font_size + self.line_spacing))
                msg_data = self.__render_font(self._font, str_tmp, self._color, msg_center)
                self.__rendered_text.append(msg_data)
                i += 1
                str_tmp = t + " "
            else:
                str_tmp += t + " "
        self.__line_count = i
        r = Rect(0, 0, 0, 0)
        r.x = self.position[0]
        r.y = self.position[1]
        r.width = max([r[1].width for r in self.__rendered_text])
        r.height = self.__line_count * (self._font_size + self.line_spacing)
        self._rect = r

    def draw(self, screen: pygame.Surface) -> None:
        for msg in self.__rendered_text:
            screen.blit(*msg)
