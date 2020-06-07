import pygame
from pygame.event import Event

from src.Interfaces.RenderObject import RenderObject


class RenderGroup(RenderObject):
    __slots__ = "group"

    def __init__(self, parent, data: dict, position: (int, int) = (0, 0)) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        self.group = data

    def __getitem__(self, key):
        return self.group[key]

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        for k, v in self.group.items():
            v.set_position((v.position[0] + self.position[0], v.position[1] + self.position[1]))

    def hide(self) -> None:
        super().hide()
        for k, v in self.group.items():
            v.hide()

    def show(self) -> None:
        super().show()
        for k, v in self.group.items():
            v.show()

    def handle_event(self, event: Event) -> None:
        for k, v in self.group.items():
            if v.is_draw:
                v.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        for k, v in self.group.items():
            if v.is_draw:
                v.draw(screen)
