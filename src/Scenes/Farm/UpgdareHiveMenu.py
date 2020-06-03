import pygame
from pygame.event import Event

from src.Database.Database import Database
from src.Scenes.Scene import Scene
from src.UI.BeeSocket import BeeSocket, BeeSocketType
from src.UI.Button import Button, ButtonState, ButtonEventType
from src.UI.DrawablesGroup import DrawablesGroup
from src.UI.ListItem import ListItem
from src.UI.ListView import ListView
from src.UI.Menu import Menu
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class UpgradeHiveMenu(Menu):
    __slots__ = ("hives_list_view", "hover_index", "__wax_amount")

    def __init__(self, parent: Scene):
        Menu.__init__(self, parent=parent, bg_name="popup3")
        self._title_label = TextLabel(parent=self, text=self.parent.localization.get_string("hives"),
                                      position=self.position, font_size=16, bold=True)
        self._title_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self._title_label.get_size()[0] / 2 + 10,
             self.position[1] + 3)
        )

        self.hives_list_view = ListView(parent=self, size=(315, 410), item_padding=(8, 8), item_distance=(0, 15),
                                        position=(self.position[0] + 35, self.position[1] + 53))

        db = Database.get_instance()
        wax = db.get_resource_by_id(1)
        self.__wax_amount = 0

        for r in self.parent.player.resources.get_bag_copy():
            if r.locale_name == wax.locale_name:
                self.__wax_amount = r.value

        self.hover_index = -1

        for h in self.parent.nest_group.buttons:
            if not h.hive:
                continue
            self.add_hive_to_list(h)

        self.parent.nest_group.stop_handle()

    def add_hive_to_list(self, h):
        h_b = Button(parent=self, normal_image_path="hive/hive1_normal.png")
        socket_group = RadioGroup()
        sock_pos = 42, 0
        for socket in h.nest_group.buttons[:-1]:
            bs = BeeSocket(parent=self, group=socket_group, socket_type=socket.full_socket_type, position=sock_pos,
                           local_id=socket.local_id)
            bs.set_image_by_state(ButtonState.LOCKED, "socket3_normal.png")
            bs.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
            if socket.is_locked:
                bs.lock()
            bs.change_image_size((28, 25))
            sock_pos = sock_pos[0] + bs.get_size()[0] + 12, sock_pos[1]
        upg_label = TextLabel(parent=self, font_size=14, text=self.parent.localization.get_string("upgrade_button"))
        upg_btn = TextButton(parent=self, text_label=upg_label, normal_image_path="start_quest_btn_normal.png",
                             text_padding=(10, 0))
        upg_btn.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")
        upg_btn.set_image_by_state(ButtonState.LOCKED, "start_quest_btn_locked.png")
        upg_btn.set_position((h_b.get_size()[0] + 20, 57))
        upg_btn.change_image_size((106, 25))
        price_label = TextLabel(parent=self, font_size=14,
                                text="{0} {1}/{2}".format(self.parent.localization.get_string("price"),
                                                          self.__wax_amount, 50))
        upg_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.upgrade_socket(socket_group=socket_group,
                                                                                     hive=h, price_label=price_label)})
        price_label.set_position((upg_btn.get_rect().right + 12, upg_btn.position[1]))
        hive_info_group = DrawablesGroup(parent=self, data={"img": h_b, "sockets": socket_group, "upg": upg_btn,
                                                            "price": price_label})
        i = ListItem(parent=self, data=hive_info_group, normal_image_path="hive_placeholder.png")
        self.hives_list_view.add_item(i)

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)
        self.hives_list_view.handle_event(event)

    def upgrade_socket(self, socket_group, hive, price_label):
        if not socket_group.current_button:
            return
        modifier = 1
        for bs in socket_group.buttons:
            if bs.full_socket_type == BeeSocketType.WARRIOR:
                modifier += 1
        price = 50 * modifier

        if self.__wax_amount < price:
            return
        modifier += 1
        price = 50 * modifier
        price_label.set_text(
            text="{0} {1}/{2}".format(self.parent.localization.get_string("price"), self.__wax_amount, price))
        socket_group.current_button.socket_type = BeeSocketType.WARRIOR
        socket_group.current_button.change_image_size((28, 25))
        for h in self.parent.nest_group.buttons:
            if h.local_id == hive.local_id:
                for s in h.nest_group.buttons:
                    if s.local_id == socket_group.current_button.local_id:
                        s.socket_type = BeeSocketType.WARRIOR
                        break
                break

        socket_group.unselect_all()

    def destroy(self):
        self.parent.nest_group.start_handle()
        super().destroy()

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.hives_list_view.draw(screen)
