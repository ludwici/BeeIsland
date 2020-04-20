from copy import copy

import pygame

from src.UI.RadioButton import RadioButton


class RadioGroup:
    def __init__(self) -> None:
        self.__buttons = []
        self.current_button = None

    @property
    def buttons(self) -> list:
        return copy(self.__buttons)

    def unselect_all(self) -> None:
        [b.unselect() for b in self.__buttons]
        self.current_button = None

    def add_button(self, b: RadioButton) -> None:
        self.__buttons.append(b)

    def draw(self, screen: pygame.Surface) -> None:
        [b.draw(screen) for b in self.__buttons]

    def handle_event(self, event) -> None:
        [b.handle_event(event) for b in self.__buttons]