import pygame

from src.UI.Button import Button


class RadioButton(Button):
    def __init__(self, parent, group, path_to_image: str, selected_image: str, is_selected: bool = False,
                 is_locked: bool = False, position: (int, int) = (0, 0)) -> None:
        Button.__init__(self, parent=parent, path_to_image=path_to_image, position=position)
        self.group = group
        self.group.add_button(self)
        self.selected_image = selected_image
        self.lock_image = "../res/images/buttons/socket3_normal.png"
        self.is_selected = is_selected
        self._is_locked = is_locked
        self._check_lock()
        self.add_action(lambda: self.select())

    def unselect(self) -> None:
        if self.is_locked:
            return
        self.is_selected = False
        self.set_image(path=self._path_to_image)

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    @is_locked.setter
    def is_locked(self, value: bool) -> None:
        self._is_locked = value
        self._check_lock()

    def _check_lock(self) -> None:
        if self._is_locked:
            self._lock()
        else:
            self._unlock()

    def _lock(self):
        self.set_image(self.lock_image)

    def _unlock(self):
        self.set_image(self._path_to_image)

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self._rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if event.button == 1:
                self.on_click()

    def select(self) -> None:
        if self.is_locked:
            return
        print("select")
        self.group.unselect_all()
        self.is_selected = True
        self.set_image(path=self.selected_image)
        self.group.current_button = self
