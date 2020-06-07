import os
from copy import copy
from enum import Enum

import pygame
from flags import Flags
from pygame.rect import Rect

from src.Interfaces.RenderObject import RenderObject
from src.Utils import resource_path


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
class Button(RenderObject):
    __slots__ = ("_current_image", "_images", "_state", "_action_list", "_action_list_rb", "_on_hover_list",
                 "_on_hover_out_list", "_can_call_out", "_can_handle_events", "_click_rect")

    def __init__(self, parent, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        self._res_dir += "/buttons"
        self._current_image = None
        self._images = dict()
        self.set_image_by_state(ButtonState.NORMAL, normal_image_path)
        self._state = None
        self.state = int(state)

        self._action_list = list()
        self._action_list_rb = list()
        self._on_hover_list = list()
        self._on_hover_out_list = list()

        self._can_call_out = False
        self._can_handle_events = True
        self._click_rect = self._rect

    def set_click_rect(self, rect: Rect) -> None:
        self._click_rect = rect

    def set_position(self, position: (int, int)) -> None:
        last_rect = copy(self._rect)
        super().set_position(position)
        if self._click_rect == last_rect:
            self._click_rect = self._rect

    def set_image_by_state(self, state: ButtonState, path: str) -> None:
        state = int(state)
        path = resource_path("{0}/{1}".format(self._res_dir, path))
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

    def change_image_size(self, size: (int, int)) -> None:
        for k, v in self._images.items():
            self._images[k] = pygame.transform.smoothscale(v, size)

        self.state = self._state

    def stop_handle(self) -> None:
        self._can_handle_events = False

    def start_handle(self) -> None:
        self._can_handle_events = True

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
    def can_handle_events(self) -> bool:
        return self._can_handle_events

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
                self._action_list.append(v)
            elif k.name == ButtonEventType.ON_HOVER_ON.name:
                self._on_hover_list.append(v)
            elif k.name == ButtonEventType.ON_HOVER_OUT.name:
                self._on_hover_out_list.append(v)
            elif k.name == ButtonEventType.ON_CLICK_RB.name:
                self._action_list_rb.append(v)
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
        if self.is_draw:
            screen.blit(self._current_image, self._rect)

    def on_hover_on(self) -> None:
        self.state |= int(ButtonState.HOVERED)
        self._can_call_out = True
        [a() for a in self._on_hover_list]

    def on_hover_out(self) -> None:
        self.state ^= int(ButtonState.HOVERED)
        [a() for a in self._on_hover_out_list]
        self._can_call_out = False

    def on_click(self) -> None:
        [a() for a in self._action_list]

    def on_click_rb(self) -> None:
        [a() for a in self._action_list_rb]

    def handle_event(self, event) -> None:
        if self.is_locked or not self._can_handle_events:
            return

        if event.type == pygame.MOUSEMOTION:
            if self._click_rect.collidepoint(event.pos):
                self.on_hover_on()
            else:
                if self._can_call_out:
                    self.on_hover_out()

        if event.type == pygame.MOUSEBUTTONUP and self.state & int(ButtonState.HOVERED):
            if event.button == 1:
                self.on_click()
            elif event.button == 3:
                self.on_click_rb()
