import pygame

from src.UI.RadioButton import RadioButton


class RadioGroup:
    __slots__ = ("__buttons", "current_button")

    def __init__(self) -> None:
        self.__buttons = []
        self.current_button = None

    def __getitem__(self, index):
        return self.__buttons[index]

    def clear(self):
        self.__buttons.clear()

    @property
    def buttons(self) -> list:
        return self.__buttons

    @property
    def unlocked_buttons(self) -> list:
        lb = []
        for b in self.__buttons:
            if not b.is_locked:
                lb.append(b)

        return lb

    @property
    def size(self) -> int:
        return len(self.__buttons)

    def unselect_all(self) -> None:
        [b.unselect() for b in self.__buttons if not b.is_locked]
        self.current_button = None

    def add_button(self, b: RadioButton) -> None:
        self.__buttons.append(b)

    def draw(self, screen: pygame.Surface) -> None:
        [b.draw(screen) for b in self.__buttons]

    def handle_event(self, event) -> None:
        [b.handle_event(event) for b in self.__buttons]
