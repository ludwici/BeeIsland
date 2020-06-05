import pygame

from src.BeeFamily.Bee import Bee
from src.BeeNest import BeeNest
from src.UI.BeeSocket import BeeSocket, BeeSocketType
from src.UI.Button import ButtonState
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioButton import RadioButton
from src.UI.RadioGroup import RadioGroup


class BeeNestButton(RadioButton):
    __slots__ = ("hive", "nest_group", "queen_socket", "__local_id", "__socket_positions")

    def __init__(self, parent, group: RadioGroup, normal_image_path: str, state: ButtonState,
                 position: (int, int) = (0, 0), local_id: int = -1) -> None:
        RadioButton.__init__(self, parent=parent, group=group, normal_image_path=normal_image_path, position=position,
                             state=state)
        self.hive = None
        self.nest_group = RadioGroup()
        self.__local_id = local_id
        self.__socket_positions = list()
        self.__socket_positions.append((-33, -41))
        self.__socket_positions.append((self.__socket_positions[0][0] + 36 + 48, self.__socket_positions[0][1]))
        self.__socket_positions.append((-9 - 48, self.__socket_positions[0][1] + 18 + 42))
        self.__socket_positions.append(
            (self.__socket_positions[2][1] + 48 + 9, self.__socket_positions[0][1] + 18 + 42))
        self.__socket_positions.append((-31, 40 + 42))
        self.__socket_positions.append((self.__socket_positions[0][0] + 36 + 48, 40 + 42))
        for i in range(6):
            bs = BeeSocket(parent=self, group=self.nest_group, local_id=i, socket_type=BeeSocketType.WORKER,
                           position=((self.position[0] + self.__socket_positions[i][0]),
                                     self.position[1] + self.__socket_positions[i][1]))
            bs.set_image_by_state(ButtonState.LOCKED, "socket3_normal.png")
            bs.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
            bs.show_select_panel(self, self.parent.player.farm.out_of_hive_bee_list)
            bs.lock()

        self.queen_socket = BeeSocket(parent=self, group=self.nest_group, socket_type=BeeSocketType.QUEEN, local_id=6,
                                      position=((self.position[0] + self.__socket_positions[2][0] + 18 + 48),
                                                self.position[1] + self.__socket_positions[2][1]))
        self.queen_socket.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
        self.queen_socket.show_select_panel(self, self.parent.player.farm.out_of_hive_bee_list)

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        for i in range(6):
            self.nest_group.buttons[i].set_position(
                ((self.position[0] + self.__socket_positions[i][0]), self.position[1] + self.__socket_positions[i][1]))
        self.queen_socket.set_position(((self.position[0] + self.__socket_positions[2][0] + 18 + 48),
                                        self.position[1] + self.__socket_positions[2][1]))

    @property
    def local_id(self) -> int:
        return self.__local_id

    def reload_sockets(self) -> None:
        for i in range(6):
            if i >= self.hive.max_size:
                self.nest_group.buttons[i].lock()
            else:
                self.nest_group.buttons[i].unlock()

    def __show_sockets(self) -> None:
        for bs in self.nest_group.buttons:
            bs.show()

    def add_bee_to_socket(self, b: Bee) -> None:
        self.hive.add_bee(b)

    def unselect(self) -> None:
        for bs in self.nest_group.buttons:
            bs.hide()
        self.nest_group.unselect_all()
        super().unselect()

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.hive and self.is_selected:
            self.nest_group.draw(screen)

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if self.hive and self.is_selected:
            self.nest_group.handle_event(event)

    def select(self) -> None:
        if self.is_selected:
            return

        if self.parent.player.already_has_hive(self.hive):
            super().select()

            self.__show_sockets()
        else:
            if self.parent.player.can_buy_new_hive:
                self.hive = BeeNest()
                self.parent.player.farm.add_hive(self.hive)
                self.set_image_by_state(ButtonState.NORMAL, "hive/hive1_normal.png")
                self.set_image_by_state(ButtonState.HOVERED, "hive/hive1_normal.png")
                self.select()
            else:
                PopupNotify(parent=self.parent, text=self.parent.localization.get_string("locked_nest"))
