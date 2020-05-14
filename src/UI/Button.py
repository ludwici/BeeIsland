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


class Button(Drawable):
    def __init__(self, parent, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self._current_image = None
        self._images = dict()
        self.set_image_by_state(ButtonState.NORMAL, normal_image_path)
        self._state = state
        self.state = state

        self.action_list = list()
        self.action_list_rb = list()
        self.on_hover_list = list()
        self.on_hover_out_list = list()

        self._can_call_out = False

    def set_image_by_state(self, state: ButtonState, path: str) -> None:
        try:
            ext = os.path.splitext(path)[1]
            if ext == ".png":
                self._images[state] = pygame.image.load(path).convert_alpha()
            else:
                self._images[state] = pygame.image.load(path)
        except:
            print("Error")

    @property
    def state(self) -> ButtonState:
        return self._state

    @state.setter
    def state(self, value: ButtonState) -> None:
        self._state = value
        if len(self._state) > 1:
            print(repr(self._state))
        try:
            if self._state & ButtonState.HOVERED or self._state & ButtonState.SELECTED:
                self._current_image = self._images[[s for s in self._state][-1]]
            else:
                self._current_image = self._images[value]
        except KeyError:
            self._current_image = self._images[ButtonState.NORMAL]
        self._rect.width = self._current_image.get_rect().width
        self._rect.height = self._current_image.get_rect().height

    @property
    def is_locked(self) -> bool:
        return self.state == ButtonState.LOCKED

    def lock(self):
        self.state = ButtonState.LOCKED

    def unlock(self):
        self.state = ButtonState.NORMAL

    def select(self):
        self.state = ButtonState.SELECTED

    def unselect(self):
        self.state = ButtonState.NORMAL

    def update(self, dt) -> None:
        pass

    def add_action(self, item: dict) -> None:
        for k, v in item.items():
            if k == ButtonEventType.ON_CLICK_LB:
                self.action_list.append(v)
            elif k == ButtonEventType.ON_HOVER_ON:
                self.on_hover_list.append(v)
            elif k == ButtonEventType.ON_HOVER_OUT:
                self.on_hover_out_list.append(v)
            elif k == ButtonEventType.ON_CLICK_RB:
                self.action_list_rb.append(v)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._current_image, self._rect)

    def on_hover_on(self):
        self.state |= ButtonState.HOVERED
        self._can_call_out = True
        [a() for a in self.on_hover_list]

    def on_hover_out(self):
        self.state ^= ButtonState.HOVERED
        [a() for a in self.on_hover_out_list]
        self._can_call_out = False

    def on_click(self) -> None:
        [a() for a in self.action_list]

    def on_click_rb(self) -> None:
        [a() for a in self.action_list_rb]

    def handle_event(self, event) -> None:
        if self.state == ButtonState.LOCKED:
            return

        if event.type == pygame.MOUSEMOTION:
            if self._rect.collidepoint(event.pos):
                self.on_hover_on()
            else:
                if self._can_call_out:
                    self.on_hover_out()

        if event.type == pygame.MOUSEBUTTONDOWN and self.state & ButtonState.HOVERED:
            if event.button == 1:
                self.on_click()
            elif event.button == 3:
                self.on_click_rb()
