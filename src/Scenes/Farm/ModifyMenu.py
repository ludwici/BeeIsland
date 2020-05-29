import itertools

import pygame
from pygame.event import Event

from src import Constants
from src.BeeFamily.Bee import Bee
from src.Interfaces.Drawable import Drawable
from src.Scenes.Scene import Scene
from src.UI.BeeSocket import BeeSocket, BeeSocketType
from src.UI.Button import Button, ButtonEventType, ButtonState
from src.UI.DrawablesGroup import DrawablesGroup
from src.UI.ListItem import ListItem
from src.UI.ListView import ListView
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class ModifyMenu(Drawable):
    __slots__ = (
        "close_btn", "_bg_image", "title_label", "socket_group", "socket1", "socket2", "upgrade_button",
        "result_socket", "info_block_image", "info_block_rect", "info_text_label", "info_group", "bee_list_view",
        "dna_image", "dna_rect")

    def __init__(self, parent: Scene) -> None:
        Drawable.__init__(self, parent=parent)
        self.close_btn = Button(parent=self, normal_image_path="close_button1.png")
        self.close_btn.set_image_by_state(ButtonState.HOVERED, "close_button1_hover.png")
        self.close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})

        self._bg_image = pygame.image.load("{0}/modify_popup1.png".format(self._res_dir)).convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height
        position = (Constants.WINDOW_W / 2 - self._bg_image.get_rect().width / 2, 70)
        self.set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

        self.title_label = TextLabel(parent=self, text=self.parent.localization.get_string("modify_title"),
                                     position=self.position, font_size=16, bold=True)
        self.title_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self.title_label.get_size()[0] / 2 + 10,
             self.position[1] + 3)
        )
        self.socket_group = RadioGroup()
        self.socket1 = BeeSocket(parent=self, normal_image_path="socket1_normal.png", socket_type=BeeSocketType.ALL,
                                 group=self.socket_group, position=(self.position[0] + 102, self.position[1] + 135))
        self.socket1.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
        self.dna_image = pygame.image.load("{0}/dna1.png".format(self._res_dir)).convert_alpha()
        self.dna_rect = self.dna_image.get_rect()
        self.dna_rect.x = self.socket1.position[0] + self.socket1.get_size()[1] + 12
        self.dna_rect.y = self.socket1.get_rect().centery - self.dna_rect.height / 2
        self.socket2 = BeeSocket(parent=self, normal_image_path="socket1_normal.png", socket_type=BeeSocketType.ALL,
                                 group=self.socket_group,
                                 position=(self.dna_rect.x + self.dna_rect.width + 7, self.socket1.position[1]))
        self.socket2.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")

        upgrade_label = TextLabel(parent=self, text=self.parent.localization.get_string("upgrade_button"), font_size=18)
        self.upgrade_button = TextButton(parent=self,
                                         normal_image_path="start_quest_btn_normal.png",
                                         text_label=upgrade_label, text_padding=(40, 4))
        self.upgrade_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")
        self.upgrade_button.set_image_by_state(ButtonState.LOCKED, "start_quest_btn_locked.png")
        self.upgrade_button.lock()
        self.upgrade_button.set_position((self.socket1.position[0],
                                          self.socket2.position[1] + self.socket2.get_size()[1] + 15))
        self.upgrade_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.upgrade()})

        self.result_socket = BeeSocket(parent=self, normal_image_path="socket1_normal.png",
                                       group=self.socket_group, position=(0, 0), socket_type=BeeSocketType.ALL)
        self.result_socket.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
        self.result_socket.set_image_by_state(ButtonState.LOCKED, "socket3_normal.png")
        self.result_socket.lock()
        self.result_socket.set_position(
            (self.upgrade_button.get_rect().centerx - self.result_socket.get_size()[1] / 2,
             self.upgrade_button.position[1] + self.upgrade_button.get_size()[1] + 15)
        )

        self.info_block_image = pygame.image.load("{0}/modify_popup1_info.png".format(self._res_dir))
        self.info_block_rect = self.info_block_image.get_rect()
        self.info_text_label = TextLabel(parent=self, text=self.parent.localization.get_string("upgrade_button"),
                                         font_size=14)

        self.info_block_rect.x = self.upgrade_button.position[0] + self.upgrade_button.get_size()[0] + 95
        self.info_block_rect.y = self.position[1] + 71
        self.info_text_label.set_position(
            (self.info_block_rect.centerx - self.info_text_label.get_size()[0] / 2, self.info_block_rect.y)
        )

        name_label = TextLabel(parent=self, font_size=14,
                               position=(self.info_block_rect.x + 25, self.info_block_rect.y + 40))

        level_label = TextLabel(parent=self, font_size=14,
                                position=(name_label.position[0],
                                          name_label.position[1] + name_label.get_size()[1]))

        xp_label = TextLabel(parent=self, font_size=14,
                             position=(
                                 level_label.position[0],
                                 level_label.position[1] + level_label.get_size()[1]))

        speed_label = TextLabel(parent=self, font_size=14,
                                position=(
                                    xp_label.position[0],
                                    xp_label.position[1] + xp_label.get_size()[1]))

        hp_label = TextLabel(parent=self, font_size=14,
                             position=(
                                 speed_label.position[0],
                                 speed_label.position[1] + speed_label.get_size()[1]))

        bonus_list_label = MultilineTextLabel(parent=self, font_size=14, line_length=230,
                                              position=(
                                                  hp_label.position[0],
                                                  hp_label.position[1] + hp_label.get_size()[1]))

        self.info_group = DrawablesGroup(parent=self,
                                         data={"b_name": name_label, "b_level": level_label, "b_exp": xp_label,
                                               "b_speed": speed_label, "b_hp": hp_label,
                                               "b_bonuses": bonus_list_label})

        self.bee_list_view = ListView(parent=self, size=(625, 253), item_padding=(15, 15), padding=(45, 24),
                                      position=(
                                          self.position[0] + 9,
                                          self.info_block_rect.y + self.info_block_rect.height - 6),
                                      )
        self.bee_list_view.set_image("{0}/modify_popup1_bee_list.png".format(self._res_dir))

        for b in itertools.chain(self.parent.player.farm.out_of_hive_bee_list,
                                 self.parent.player.farm.bees_from_all_hives):
            self.add_bee_to_list(b)

        self.socket1.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket()})
        self.socket1.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_bee_from_socket(self.socket1)})
        self.socket1.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.reload_bee_info(self.socket1.bee)})

        self.socket2.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket()})
        self.socket2.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_bee_from_socket(self.socket2)})
        self.socket2.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.reload_bee_info(self.socket2.bee)})

        self.clear_bee_info()

    def upgrade(self):
        self.upgrade_button.lock()
        self.parent.player.farm.remove_out_of_hive_bee(self.socket1.bee)
        self.parent.player.farm.remove_out_of_hive_bee(self.socket2.bee)
        del self.socket1.bee
        del self.socket2.bee
        self.result_socket.unlock()
        self.result_socket.select()

    def add_bee_to_list(self, b: Bee) -> None:
        i = ListItem(parent=self, data=b, normal_image_path="holder1.png")
        i.set_image_by_state(ButtonState.LOCKED, "holder1_lock.png")
        i.set_image_by_state(ButtonState.HOVERED, "holder1_hover.png")
        i.add_action({ButtonEventType.ON_CLICK_LB: lambda e=i: self.select_bee(e)})
        i.add_action({ButtonEventType.ON_HOVER_ON: lambda e=i.data: self.reload_bee_info(e)})
        i.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.reload_bee_info()})
        self.bee_list_view.add_item(i)

    def remove_bee_from_socket(self, socket: BeeSocket) -> None:
        socket.select()
        if self.socket_group.current_button.bee:
            self.add_bee_to_list(self.socket_group.current_button.bee)
            del self.socket_group.current_button.bee
            self.clear_bee_info()
            self.upgrade_button.lock()

    def select_bee(self, list_item: ListItem) -> None:
        if self.socket_group.current_button:
            if self.socket_group.current_button.bee:
                self.remove_bee_from_socket(self.socket_group.current_button)

            self.socket_group.current_button.bee = list_item.data
            self.bee_list_view.remove_item(list_item)

        if self.socket1.bee and self.socket2.bee:
            self.upgrade_button.unlock()
        else:
            self.upgrade_button.lock()

        self.reload_bee_info()

    def add_bee_to_socket(self) -> None:
        if self.socket_group.current_button:
            if self.socket_group.current_button.bee:
                self.reload_bee_info()
            else:
                self.clear_bee_info()

    def clear_bee_info(self) -> None:
        for k, v in self.info_group.group.items():
            v.set_text(text=self.parent.localization.get_string(k))
        self.set_info_position()

    def set_info_position(self):
        self.info_group["b_name"].set_position((self.info_block_rect.x + 25, self.info_block_rect.y + 40))

        self.info_group["b_level"].set_position((self.info_group["b_name"].position[0],
                                                 self.info_group["b_name"].position[1]
                                                 + self.info_group["b_name"].get_size()[1]))
        self.info_group["b_exp"].set_position((self.info_group["b_level"].position[0],
                                               self.info_group["b_level"].position[1]
                                               + self.info_group["b_level"].get_size()[1]))
        self.info_group["b_speed"].set_position((self.info_group["b_exp"].position[0],
                                                 self.info_group["b_exp"].position[1]
                                                 + self.info_group["b_exp"].get_size()[1]))
        self.info_group["b_hp"].set_position((self.info_group["b_speed"].position[0],
                                              self.info_group["b_speed"].position[1]
                                              + self.info_group["b_speed"].get_size()[1]))
        self.info_group["b_bonuses"].set_position((self.info_group["b_hp"].position[0],
                                                   self.info_group["b_hp"].position[1]
                                                   + self.info_group["b_hp"].get_size()[1]))

    def reload_bee_info(self, b: Bee = None) -> None:
        if b is None and self.socket_group.current_button:
            b = self.socket_group.current_button.bee
        if not b:
            return

        self.info_group["b_name"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_name"), b.name))

        self.info_group["b_level"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_level"), b.current_level)
        )

        self.info_group["b_exp"].set_text(
            text="{0} {1}/{2}".format(self.parent.localization.get_string("b_exp"), b.current_xp, b.max_xp)
        )

        self.info_group["b_speed"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_speed"), b.speed))

        self.info_group["b_hp"].set_text(
            text="{0} {1}/{2}".format(self.parent.localization.get_string("b_hp"), b.current_hp, b.max_hp)
        )

        self.info_group["b_bonuses"].set_text(
            text="{0} {1}".format(self.parent.localization.get_string("b_bonuses"), b.bonus)
        )

    def destroy(self) -> None:
        self.parent.remove_drawable(self)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
        self.close_btn.draw(screen)
        self.title_label.draw(screen)
        self.socket_group.draw(screen)
        self.upgrade_button.draw(screen)
        screen.blit(self.dna_image, self.dna_rect)
        screen.blit(self.info_block_image, self.info_block_rect)
        self.info_text_label.draw(screen)
        self.bee_list_view.draw(screen)
        self.info_group.draw(screen)

    def handle_event(self, event: Event) -> None:
        self.close_btn.handle_event(event)
        self.socket_group.handle_event(event)
        self.upgrade_button.handle_event(event)
        self.bee_list_view.handle_event(event)
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         self.bee_list_view.item_padding = (30, 8)
