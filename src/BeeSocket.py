import pygame

from src.BeeFamily.Bee import Bee
from src.UI.Button import ButtonState
from src.UI.RadioButton import RadioButton


class BeeSocket(RadioButton):
    def __init__(self, parent, group, normal_image_path: str, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL) -> None:
        RadioButton.__init__(self, parent=parent, group=group, normal_image_path=normal_image_path,
                             position=position, state=state)
        self._bee = None

    @property
    def bee(self):
        return self._bee

    @bee.setter
    def bee(self, b: Bee):
        self._bee = b
        self._bee.get_rect().center = self._rect.center

    @bee.deleter
    def bee(self):
        self._bee = None

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self._bee:
            self._bee.draw(screen)
