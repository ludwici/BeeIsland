import pygame
from pygame.event import Event

from src.Interfaces.Drawable import Drawable


class DrawablesGroup(Drawable):
    __slots__ = "group"

    def __init__(self, parent, data: dict, position: (int, int) = (0, 0)) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self.group = data
        # self.set_position(position)

    def __getitem__(self, key):
        return self.group[key]

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        for k, v in self.group.items():
            v.set_position((v.position[0] + self.position[0], v.position[1] + self.position[1]))

    def handle_event(self, event: Event) -> None:
        for k, v in self.group.items():
            if v.is_draw:
                v.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        for k, v in self.group.items():
            if v.is_draw:
                v.draw(screen)
