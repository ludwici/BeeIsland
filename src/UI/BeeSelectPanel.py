from copy import copy

import pygame

from BeeFamily.Bee import Bee
from Interfaces.Drawable import Drawable
from UI.Button import Button, ButtonState, ButtonEventType
from UI.DrawablesGroup import DrawablesGroup
from UI.ListItem import ListItem
from UI.ListView import ListView
from UI.MultilineTextLabel import MultilineTextLabel
from UI.TextLabel import TextLabel


class BeeSelectPanel(Drawable):
    def __init__(self, parent, socket, bee_list: list, destination=None, position: (int, int) = (0, 0)):
        Drawable.__init__(self, parent=parent, position=position)
        while self.parent.find_drawable_by_type(BeeSelectPanel):
            self.parent.remove_drawable(self.parent.find_drawable_by_type(BeeSelectPanel))
        self.__bee_list = bee_list
        self.__allowable_position_x = 100
        self.__allowable_position_y = 0
        self.__socket = socket
        self.__destination = destination
        self.__socket.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_from_socket(self.__socket)})
        self.parent.add_drawable(self)
        self.close_btn = Button(parent=self, normal_image_path="../res/images/buttons/close_button1.png")
        self.close_btn.set_image_by_state(ButtonState.HOVERED, "../res/images/buttons/close_button1_hover.png")
        self.close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})
        self._bg_image = pygame.image.load("../res/images/select_bee_panel.png").convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height
        self.bee_list_view = ListView(parent=self, position=(0, 0), padding=(33, 36), item_padding=(15, 10),
                                      size=(308, 170))

        name_label = TextLabel(parent=self, position=(self.position[0] + 323, self.position[1] + 25),
                               font_name="segoeprint", font_size=14, color=(159, 80, 17))

        level_label = TextLabel(parent=self,
                                position=(name_label.position[0], name_label.position[1] + name_label.get_size()[1]),
                                font_name="segoeprint", font_size=14, color=(159, 80, 17))

        xp_label = TextLabel(parent=self,
                             position=(level_label.position[0], level_label.position[1] + level_label.get_size()[1]),
                             font_name="segoeprint", font_size=14, color=(159, 80, 17))

        speed_label = TextLabel(parent=self,
                                position=(xp_label.position[0], xp_label.position[1] + xp_label.get_size()[1]),
                                font_name="segoeprint", font_size=14, color=(159, 80, 17))

        hp_label = TextLabel(parent=self,
                             position=(speed_label.position[0], speed_label.position[1] + speed_label.get_size()[1]),
                             font_name="segoeprint", font_size=14, color=(159, 80, 17))

        bonus_list_label = MultilineTextLabel(parent=self, text="",
                                              position=(hp_label.position[0],
                                                        hp_label.position[1] + hp_label.get_size()[1]),
                                              font_name="segoeprint", font_size=14,
                                              color=(159, 80, 17), line_length=230)
        self.info_group = DrawablesGroup(parent=self,
                                         data={"b_name": name_label, "b_level": level_label, "b_exp": xp_label,
                                               "b_speed": speed_label, "b_hp": hp_label,
                                               "b_bonuses": bonus_list_label})
        for b in self.__bee_list:
            self.add_bee_to_list(b)

        self.show_info(self.__socket.bee)

    def destroy(self):
        self.parent.remove_drawable(self)

    def remove_from_socket(self, socket):
        if socket.bee:
            copied = copy(socket.bee)
            self.__bee_list.append(copied)
            self.add_bee_to_list(copied)
            del socket.bee

    def add_bee_to_socket(self, item: ListItem):
        self.remove_from_socket(self.__socket)
        b = copy(item.data)
        self.__socket.bee = b
        if self.__destination:
            self.__destination.add_bee(b)
        self.__bee_list.remove(item.data)
        self.bee_list_view.remove_item(item)

    def add_bee_to_list(self, b: Bee):
        i = ListItem(parent=self, data=b, normal_image_path="../res/images/holder1.png")
        i.set_image_by_state(ButtonState.LOCKED, "../res/images/holder1_lock.png")
        i.set_image_by_state(ButtonState.HOVERED, "../res/images/holder1_hover.png")
        i.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket(i)})
        i.add_action({ButtonEventType.ON_HOVER_ON: lambda: self.show_info(i.data)})
        i.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.show_info(self.__socket.bee)})
        self.bee_list_view.add_item(i)

    def _check_position(self, position: (int, int)) -> (int, int):
        correct_position_x, correct_position_y = position
        if position[0] < self.__allowable_position_x:
            correct_position_x = self.__allowable_position_x + 5

        if position[1] < self.__allowable_position_y:
            correct_position_y = position[1] + self.get_size()[1] + 20

        return correct_position_x, correct_position_y

    def set_position(self, position: (int, int)) -> None:
        super().set_position(self._check_position(position))
        self.close_btn.set_position(position=(self._rect.topright[0] - 62, self._rect.topright[1] - 1))
        self.bee_list_view.set_position(self.position)
        self.info_group.set_position(self.position)

    def handle_event(self, event) -> None:
        self.close_btn.handle_event(event)
        self.bee_list_view.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
        self.close_btn.draw(screen)
        self.bee_list_view.draw(screen)
        self.info_group.draw(screen)

    def show_info(self, b: Bee):
        if not b:
            return
        self.info_group["b_name"].set_text(text="{0} {1}".format(self.parent.localization.get_string("b_name"), b.name))

        self.info_group["b_level"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_level"), b.current_level)
        )
        self.info_group["b_level"].set_position((self.info_group["b_name"].position[0],
                                                 self.info_group["b_name"].position[1]
                                                 + self.info_group["b_name"].get_size()[1]))

        self.info_group["b_exp"].set_text(
            text="{0} {1}/{2}".format(self.parent.localization.get_string("b_exp"), b.current_xp, b.max_xp)
        )
        self.info_group["b_exp"].set_position((self.info_group["b_level"].position[0],
                                               self.info_group["b_level"].position[1]
                                               + self.info_group["b_level"].get_size()[1]))

        self.info_group["b_speed"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_speed"), b.speed))
        self.info_group["b_speed"].set_position((self.info_group["b_exp"].position[0],
                                                 self.info_group["b_exp"].position[1]
                                                 + self.info_group["b_exp"].get_size()[1]))

        self.info_group["b_hp"].set_text(
            text="{0} {1}/{2}".format(self.parent.localization.get_string("b_hp"), b.current_hp, b.max_hp)
        )
        self.info_group["b_hp"].set_position((self.info_group["b_speed"].position[0],
                                              self.info_group["b_speed"].position[1]
                                              + self.info_group["b_speed"].get_size()[1]))

        self.info_group["b_bonuses"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_bonuses"), "+10% очков")
        )
        self.info_group["b_bonuses"].set_position((self.info_group["b_hp"].position[0],
                                                   self.info_group["b_hp"].position[1]
                                                   + self.info_group["b_hp"].get_size()[1]))
