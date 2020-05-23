import pygame

from UI.RadioButton import RadioButton
from src.BeeNest import BeeNest
from src.BeeSocket import BeeSocket
from src.UI.Button import ButtonState
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioGroup import RadioGroup


class BeeNestButton(RadioButton):
    def __init__(self, parent, group: RadioGroup, normal_image_path: str, state: ButtonState,
                 position: (int, int) = (0, 0)) -> None:
        RadioButton.__init__(self, parent=parent, group=group, normal_image_path=normal_image_path, position=position,
                             state=state)
        self.hive = None
        self.nest_group = RadioGroup()

    def __show_sockets(self) -> None:
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
            # bs.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.show_bee_select_panel()})
            # bs.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")
            bs.show_select_panel(self.parent, self.parent.player.farm.out_of_hive_bee_list)
            bs.unlock()
        self.queen_socket = BeeSocket(parent=self, group=self.nest_group,
                                      normal_image_path="../res/images/buttons/socket4_normal.png",
                                      position=((self.position[0] + positions[2][0] + 18 + 48),
                                                self.position[1] + positions[2][1]))
        # self.queen_socket.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.show_bee_select_panel()})
        self.queen_socket.show_select_panel(self.parent, self.parent.player.farm.out_of_hive_bee_list)
        # self.queen_socket.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")

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
        if not self.parent.player.already_has_hive(self.hive):
            if self.parent.player.can_buy_new_hive:
                super().select()
                self.hive = BeeNest()
                self.parent.player.farm.add_hive(self.hive)
                self.set_image_by_state(ButtonState.NORMAL, "../res/images/bee/hive/hive1_normal.png")
                self.set_image_by_state(ButtonState.HOVERED, "../res/images/bee/hive/hive1_normal.png")
                self.__show_sockets()
            else:
                PopupNotify.create(scene=self.parent, text=self.parent.localization.get_string("locked_nest"))
        else:
            super().select()
            self.__show_sockets()
