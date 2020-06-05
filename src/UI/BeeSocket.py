from copy import copy
from enum import Enum

import pygame

from src.BeeFamily.Bee import Bee
from src.BeeFamily.BeeQueen import BeeQueen
from src.BeeFamily.BeeWarrior import BeeWarrior
from src.BeeFamily.BeeWorker import BeeWorker
from src.UI.BeeSelectPanel import BeeSelectPanel
from src.UI.Button import ButtonState, Button, ButtonEventType
from src.UI.RadioButton import RadioButton


class BeeSocketType(Enum):
    ALL = 0,
    WORKER = BeeWorker,
    WARRIOR = BeeWarrior,
    QUEEN = BeeQueen


class BeeSocket(RadioButton):
    __slots__ = ("_bee", "__local_id", "__socket_type", "__can_change_id")

    def __init__(self, parent, group, socket_type: BeeSocketType, position: (int, int) = (0, 0),
                 state: ButtonState = ButtonState.NORMAL, local_id: int = -1, can_change_id: bool = True) -> None:
        self.__socket_type = socket_type
        if self.__socket_type == BeeSocketType.ALL:
            normal_image_path = "WORKER.png"
        else:
            normal_image_path = "{0}.png".format(self.__socket_type.name)

        RadioButton.__init__(self, parent=parent, group=group, normal_image_path=normal_image_path,
                             position=position, state=state)
        self.__can_change_id = can_change_id
        self.__local_id = local_id
        self._bee = None
        if self.__local_id != -1:
            try:
                for b in self.parent.hive.bee_list:
                    if b.socket_id == self.__local_id:
                        self.bee = b
                        break
            except AttributeError:
                pass

    @property
    def full_socket_type(self):
        return self.__socket_type

    @property
    def socket_type(self):
        try:
            return copy(self.__socket_type.value[0])
        except TypeError:
            return self.__socket_type.value

    @property
    def local_id(self) -> int:
        return self.__local_id

    @socket_type.setter
    def socket_type(self, value: BeeSocketType) -> None:
        self.__socket_type = value
        if self.__socket_type == BeeSocketType.ALL:
            normal_image_path = "WORKER.png"
        else:
            normal_image_path = "{0}.png".format(self.__socket_type.name)
        self.set_image_by_state(ButtonState.NORMAL, normal_image_path)

    @property
    def bee(self):
        return self._bee

    def show(self) -> None:
        super().show()
        if self._bee:
            self._bee.get_rect().center = self._rect.center

    @bee.setter
    def bee(self, b: Bee):
        self._bee = b
        self._bee.get_rect().center = self._rect.center
        if self.__can_change_id:
            self._bee.socket_id = self.__local_id

        if isinstance(b, BeeQueen):
            self.parent.hive.add_queen()
            self.parent.reload_sockets()

    @bee.deleter
    def bee(self):
        if isinstance(self._bee, BeeQueen):
            self.parent.hive.remove_queen()
            self.parent.reload_sockets()
        self._bee = None

    @Button.register_event(ButtonEventType.ON_CLICK_RB)
    def remove(self, menu):
        if self._bee:
            self._bee.remove_bonus(menu.quest)

    @Button.register_event(ButtonEventType.ON_CLICK_LB)
    def show_select_panel(self, parent, bee_list) -> None:
        bsp = BeeSelectPanel(parent=parent, socket=self, bee_list=bee_list)
        bsp.set_position((self.position[0] - bsp.size[0] / 2, self.position[1] - bsp.size[1]))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self._bee:
            self._bee.draw(screen)
