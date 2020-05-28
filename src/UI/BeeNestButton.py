import pygame

from src.BeeFamily.Bee import Bee
from src.BeeNest import BeeNest
from src.UI.BeeSocket import BeeSocket
from src.UI.Button import ButtonState
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioButton import RadioButton
from src.UI.RadioGroup import RadioGroup


class BeeNestButton(RadioButton):
    __slots__ = ("hive", "nest_group", "queen_socket")

    def __init__(self, parent, group: RadioGroup, normal_image_path: str, state: ButtonState,
                 position: (int, int) = (0, 0)) -> None:
        RadioButton.__init__(self, parent=parent, group=group, normal_image_path=normal_image_path, position=position,
                             state=state)
        self.hive = None
        self.nest_group = RadioGroup()

    def __show_sockets(self) -> None:
        self.nest_group.clear()
        positions = list()
        positions.append((-33, -41))
        positions.append((positions[0][0] + 36 + 48, positions[0][1]))
        positions.append((-9 - 48, positions[0][1] + 18 + 42))
        positions.append((positions[2][1] + 48 + 9, positions[0][1] + 18 + 42))
        positions.append((-31, 40 + 42))
        positions.append((positions[0][0] + 36 + 48, 40 + 42))
        for i in range(6):
            bs = BeeSocket(parent=self, group=self.nest_group,
                           normal_image_path="../res/images/buttons/socket1_normal.png",
                           position=((self.position[0] + positions[i][0]), self.position[1] + positions[i][1]))
            bs.set_image_by_state(ButtonState.LOCKED, "../res/images/buttons/socket3_normal.png")
            bs.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")
            bs.show_select_panel(self, self.parent.player.farm.out_of_hive_bee_list)
            if i >= self.hive.max_size:
                bs.lock()
        self.queen_socket = BeeSocket(parent=self, group=self.nest_group,
                                      normal_image_path="../res/images/buttons/socket4_normal.png",
                                      position=((self.position[0] + positions[2][0] + 18 + 48),
                                                self.position[1] + positions[2][1]))
        self.queen_socket.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")
        self.queen_socket.show_select_panel(self, self.parent.player.farm.out_of_hive_bee_list)

    def add_bee_to_socket(self, b: Bee):
        self.hive.add_bee(b)

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
                self.set_image_by_state(ButtonState.NORMAL, "../res/images/bee/hive/hive1_normal.png")
                self.set_image_by_state(ButtonState.HOVERED, "../res/images/bee/hive/hive1_normal.png")
                self.select()
            else:
                PopupNotify.create(scene=self.parent, text=self.parent.localization.get_string("locked_nest"))
