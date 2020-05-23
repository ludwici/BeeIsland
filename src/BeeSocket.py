import pygame

from Scenes.BeeSelectPanel import BeeSelectPanel
from src.BeeFamily.Bee import Bee
from src.UI.Button import ButtonState, Button, ButtonEventType
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

    @Button.register_event(ButtonEventType.ON_CLICK_LB)
    def show_select_panel(self, parent=None, bee_list=None) -> None:
        bsp = BeeSelectPanel(parent=parent, bee_list=bee_list)
        bsp.set_position((self.position[0] - bsp.get_size()[0] / 2, self.position[1] - bsp.get_size()[1]))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self._bee:
            self._bee.draw(screen)
