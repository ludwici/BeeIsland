import pygame

from src.BeeFamily.Bee import Bee
from src.Interfaces.RenderObject import RenderObject
from src.UI.Button import Button, ButtonState, ButtonEventType
from src.UI.ListItem import ListItem
from src.UI.ListView import ListView
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.RenderGroup import RenderGroup
from src.UI.TextLabel import TextLabel


class BeeSelectPanel(RenderObject):
    __slots__ = (
        "__bee_list", "__allowable_position_x", "__allowable_position_y", "__socket", "close_btn",
        "_bg_image", "bee_list_view", "info_group", "__scene")

    def __init__(self, parent, socket, bee_list: list, position: (int, int) = (0, 0)) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        self.__bee_list = bee_list
        self.__allowable_position_x = 100
        self.__allowable_position_y = 0
        self.__socket = socket
        self.__socket.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_from_socket(self.__socket)})
        self.__scene = parent.parent
        self.__scene.add_render(self)
        self.close_btn = Button(parent=self, normal_image_path="close_button1.png")
        self.close_btn.set_image_by_state(ButtonState.HOVERED, "close_button1_hover.png")
        self.close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})
        self._bg_image = pygame.image.load("{0}/select_bee_panel.png".format(self._res_dir)).convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height
        self.bee_list_view = ListView(parent=self, position=(0, 0), padding=(23, 21), item_padding=(10, 10),
                                      size=(308, 170), item_distance=(10, 15))

        name_label = TextLabel(parent=self, position=(self.position[0] + 323, self.position[1] + 30), font_size=14)

        level_label = TextLabel(parent=self, font_size=14,
                                position=(name_label.position[0], name_label.position[1] + name_label.size[1]))

        xp_label = TextLabel(parent=self, font_size=14,
                             position=(level_label.position[0], level_label.position[1] + level_label.size[1]))

        speed_label = TextLabel(parent=self, font_size=14,
                                position=(xp_label.position[0], xp_label.position[1] + xp_label.size[1]))

        hp_label = TextLabel(parent=self, font_size=14,
                             position=(speed_label.position[0], speed_label.position[1] + speed_label.size[1]))

        bonus_list_label = MultilineTextLabel(parent=self, font_size=14, line_length=190,
                                              position=(hp_label.position[0],
                                                        hp_label.position[1] + hp_label.size[1]))
        self.info_group = RenderGroup(parent=self,
                                      data={"b_name": name_label, "b_level": level_label, "b_exp": xp_label,
                                            "b_speed": speed_label, "b_hp": hp_label,
                                            "b_bonus": bonus_list_label})
        for b in self.__bee_list:
            self.add_bee_to_list(b)

        self.show_info(self.__socket.bee)

    def destroy(self) -> None:
        self.__scene.remove_render(self)

    def remove_from_socket(self, socket) -> None:
        if socket.bee:
            self.__bee_list.append(socket.bee)
            self.add_bee_to_list(socket.bee)
            del socket.bee

    def add_bee_to_socket(self, item: ListItem) -> None:
        self.remove_from_socket(self.__socket)
        b = item.data
        self.__socket.bee = b

        self.parent.add_bee_to_socket(b)

        self.__bee_list.remove(item.data)
        self.bee_list_view.remove_item(item)

    def add_bee_to_list(self, b: Bee) -> None:
        if type(b) != self.__socket.socket_type:
            return

        i = ListItem(parent=self, data=b, normal_image_path="holder1.png")
        i.set_image_by_state(ButtonState.LOCKED, "holder1_lock.png")
        i.set_image_by_state(ButtonState.HOVERED, "holder1_hover.png")
        i.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket(i)})
        i.add_action({ButtonEventType.ON_HOVER_ON: lambda: self.show_info(i.data)})
        i.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.show_info(self.__socket.bee)})
        self.bee_list_view.add_item(i)

    def _check_position(self, position: (int, int)) -> (int, int):
        correct_position_x, correct_position_y = position
        if position[0] < self.__allowable_position_x:
            correct_position_x = self.__allowable_position_x + 5

        if position[1] < self.__allowable_position_y:
            correct_position_y = position[1] + self.size[1] + 20

        return correct_position_x, correct_position_y

    def set_position(self, position: (int, int)) -> None:
        super().set_position(self._check_position(position))
        self.close_btn.set_position(position=(self._rect.topright[0] - 62, self._rect.topright[1] - 1))
        self.bee_list_view.set_position(self.position)
        self.info_group.set_position(self.position)

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self._rect.collidepoint(event.pos):
                if event.button == 1:
                    self.destroy()

        self.close_btn.handle_event(event)
        self.bee_list_view.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
        self.close_btn.draw(screen)
        self.bee_list_view.draw(screen)
        self.info_group.draw(screen)

    def show_info(self, b: Bee) -> None:
        if not b:
            return

        # self.info_group["b_bonus"].show()
        try:
            self.info_group["b_name"].set_text(
                text="{0} {1}".format(self.__scene.localization.get_string("b_name"), b.name))

            self.info_group["b_level"].set_text(
                text="{0} {1}".format(self.__scene.localization.get_string("b_level"), b.current_level)
            )
            self.info_group["b_level"].set_position((self.info_group["b_name"].position[0],
                                                     self.info_group["b_name"].position[1]
                                                     + self.info_group["b_name"].size[1] - 5))

            self.info_group["b_exp"].set_text(
                text="{0} {1}/{2}".format(self.__scene.localization.get_string("b_exp"), b.current_xp, b.max_xp)
            )
            self.info_group["b_exp"].set_position((self.info_group["b_level"].position[0],
                                                   self.info_group["b_level"].position[1]
                                                   + self.info_group["b_level"].size[1] - 5))

            self.info_group["b_speed"].set_text(
                text="{0} {1}".format(self.__scene.localization.get_string("b_speed"), b.speed))
            self.info_group["b_speed"].set_position((self.info_group["b_exp"].position[0],
                                                     self.info_group["b_exp"].position[1]
                                                     + self.info_group["b_exp"].size[1] - 5))

            self.info_group["b_hp"].set_text(
                text="{0} {1}/{2}".format(self.__scene.localization.get_string("b_hp"), b.current_hp, b.max_hp)
            )
            self.info_group["b_hp"].set_position((self.info_group["b_speed"].position[0],
                                                  self.info_group["b_speed"].position[1]
                                                  + self.info_group["b_speed"].size[1] - 5))

            self.info_group["b_bonus"].set_text(
                text="{0} {1}".format(self.__scene.localization.get_string("b_bonus"), b.bonus.description)
            )
            self.info_group["b_bonus"].set_position((self.info_group["b_hp"].position[0],
                                                     self.info_group["b_hp"].position[1]
                                                     + self.info_group["b_hp"].size[1] - 5))
        except AttributeError:
            pass
        except KeyError as ky:
            field = str(ky).replace('\'', '')
            self.info_group[field].hide()
