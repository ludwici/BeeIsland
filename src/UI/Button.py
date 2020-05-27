import os
from enum import Enum

import pygame
from flags import Flags

from src.Interfaces.Drawable import Drawable


class ButtonEventType(Enum):
    ON_CLICK_LB = 1,
    ON_HOVER_ON = 2,
    ON_HOVER_OUT = 3,
    ON_CLICK_RB = 4


class ButtonState(Flags):
    LOCKED = 0,
    NORMAL = 1,
    HOVERED = 2,
    SELECTED = 4


# TODO: Mixed Strategy pattern
class Button(Drawable):
    __slots__ = ("_current_image", "_images", "_state", "__action_list", "__action_list_rb", "__on_hover_list",
                 "__on_hover_out_list", "_can_call_out")

    def __init__(self, parent, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self._current_image = None
        self._images = dict()
        self.set_image_by_state(ButtonState.NORMAL, normal_image_path)
        self._state = None
        self.state = int(state)

        self.__action_list = list()
        self.__action_list_rb = list()
        self.__on_hover_list = list()
        self.__on_hover_out_list = list()

        self._can_call_out = False

    def set_image_by_state(self, state: ButtonState, path: str) -> None:
        state = int(state)
        try:
            ext = os.path.splitext(path)[1]
            if ext == ".png":
                self._images[state] = pygame.image.load(path).convert_alpha()
            else:
                self._images[state] = pygame.image.load(path)
        except pygame.error:
            raise FileNotFoundError("image {0} not found".format(path))

    @property
    def state(self) -> ButtonState:
        return self._state

    @state.setter
    def state(self, value: ButtonState) -> None:
        self._state = value
        try:
            if self._state & int(ButtonState.HOVERED) or self._state & int(ButtonState.SELECTED):
                val = [s for s in ButtonState(value)][-1]
                self._current_image = self._images[int(val)]
            else:
                self._current_image = self._images[value]
        except KeyError:
            self._current_image = self._images[int(ButtonState.NORMAL)]
        self._rect.width = self._current_image.get_rect().width
        self._rect.height = self._current_image.get_rect().height

    @property
    def is_locked(self) -> bool:
        return self.state == int(ButtonState.LOCKED)

    @property
    def is_selected(self) -> bool:
        return self._state & int(ButtonState.SELECTED)

    def lock(self) -> None:
        self.state = int(ButtonState.LOCKED)

    def unlock(self) -> None:
        self.state = int(ButtonState.NORMAL)

    def select(self) -> None:
        self.state = int(ButtonState.SELECTED)

    def unselect(self) -> None:
        self.state = int(ButtonState.NORMAL)

    def update(self, dt) -> None:
        pass

    def add_action(self, item: dict, *args) -> None:
        for k, v in item.items():
            if k.name == ButtonEventType.ON_CLICK_LB.name:
                self.__action_list.append(v)
            elif k.name == ButtonEventType.ON_HOVER_ON.name:
                self.__on_hover_list.append(v)
            elif k.name == ButtonEventType.ON_HOVER_OUT.name:
                self.__on_hover_out_list.append(v)
            elif k.name == ButtonEventType.ON_CLICK_RB.name:
                self.__action_list_rb.append(v)
            else:
                raise KeyError("Invalid flag: {0}".format(k))

    @classmethod
    def register_event(cls, state: ButtonEventType):
        def process(handler):
            def wrapper(*args):
                args[0].add_action({state: lambda: handler(*args)})

            return wrapper

        return process

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._current_image, self._rect)

    def on_hover_on(self) -> None:
        self.state |= int(ButtonState.HOVERED)
        self._can_call_out = True
        [a() for a in self.__on_hover_list]

    def on_hover_out(self) -> None:
        self.state ^= int(ButtonState.HOVERED)
        [a() for a in self.__on_hover_out_list]
        self._can_call_out = False

    def on_click(self) -> None:
        [a() for a in self.__action_list]

    def on_click_rb(self) -> None:
        [a() for a in self.__action_list_rb]

    def handle_event(self, event) -> None:
        if self.is_locked:
            return

        if event.type == pygame.MOUSEMOTION:
            if self._rect.collidepoint(event.pos):
                self.on_hover_on()
            else:
                if self._can_call_out:
                    self.on_hover_out()

        if event.type == pygame.MOUSEBUTTONUP and self.state & int(ButtonState.HOVERED):
            if event.button == 1:
                self.on_click()
            elif event.button == 3:
                self.on_click_rb()
