from copy import copy

import pygame

from src import Constants
from src.InGameResources.Resource import Resource
from src.Interfaces.Drawable import Drawable
from src.Scenes.Scene import Scene
from src.UI.Button import Button, ButtonState, ButtonEventType
from src.UI.DrawablesGroup import DrawablesGroup
from src.UI.ListItem import ListItem
from src.UI.ListView import ListView
from src.UI.PopupNotify import PopupNotify
from src.UI.TextLabel import TextLabel


class BagMenu(Drawable):
    __slots__ = (
        "close_btn", "_bg_image", "_rect", "title_label", "resource_list_view", "name_res_label", "amount_res_label",
        "can_show_hint", "sec_to_show", "hint_text")

    def __init__(self, parent: Scene) -> None:
        Drawable.__init__(self, parent=parent)
        self.close_btn = Button(parent=self, normal_image_path="close_button1.png")
        self.close_btn.set_image_by_state(ButtonState.HOVERED, "close_button1_hover.png")
        self.close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})

        self._bg_image = pygame.image.load("{0}/popup3.png".format(self._res_dir)).convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height
        position = (Constants.WINDOW_W / 2 - self._bg_image.get_rect().width / 2, 70)
        self.set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

        self.title_label = TextLabel(parent=self, text=self.parent.localization.get_string("bag_title"),
                                     position=self.position, font_size=16, bold=True)
        self.title_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self.title_label.get_size()[0] / 2 + 10,
             self.position[1] + 3)
        )

        self.resource_list_view = ListView(parent=self, position=(self.position[0] + 35, self.position[1] + 85),
                                           size=(401, 417), padding=(-9, 0), item_padding=(9, 0))
        self.resource_list_view.set_image("{0}/bag/bg.png".format(self._res_dir))

        self.name_res_label = TextLabel(parent=self, text=self.parent.localization.get_string("res_name_label"),
                                        position=(self.resource_list_view.position[0], position[1] + 56), font_size=14,
                                        bold=True)
        self.name_res_label.set_position((self.name_res_label.position[0] + self.resource_list_view.get_size()[0] / 4
                                          - self.name_res_label.get_size()[0] / 2, self.name_res_label.position[1]))

        self.amount_res_label = TextLabel(parent=self, text=parent.localization.get_string("amount_res_label"),
                                          position=(self.resource_list_view.position[0],
                                                    self.position[1] + 56), font_size=14, bold=True)
        self.amount_res_label.set_position(
            (self.amount_res_label.position[0] + self.resource_list_view.get_size()[0] / 2
             + self.amount_res_label.get_size()[0] / 2, self.amount_res_label.position[1])
        )
        self.can_show_hint = False
        self.sec_to_show = 2
        self.hint_text = ""
        bag_copy = copy(self.parent.player.resources.get_bag_copy())
        for i in range(len(bag_copy)):
            self.add_resource_to_list(bag_copy[i], i)

    def show_hint(self, text: str) -> None:
        if self.can_show_hint:
            return
        self.hint_text = text
        self.can_show_hint = True

    def update(self, dt: float) -> None:
        if self.can_show_hint:
            self.sec_to_show -= (1 * dt) / 1000
            if self.sec_to_show <= 0:
                self.stop_hint()
                self.parent.remove_drawable(self.parent.find_drawable_by_type(PopupNotify))
                PopupNotify(parent=self.parent, text=self.hint_text)

    def stop_hint(self) -> None:
        self.sec_to_show = 2
        self.can_show_hint = False

    def add_resource_to_list(self, r: Resource, index: int) -> None:
        r_label = TextLabel(parent=self, text=r.locale_name, font_size=12)
        amount_label = TextLabel(parent=self, text="{0} / {1}".format(str(r.value), str(r.max_value)), font_size=12)
        group = DrawablesGroup(parent=self, data={"name": r_label, "amount": amount_label})
        list_elem = index % 2
        i = ListItem(parent=self, data=group, normal_image_path="res_placeholder{0}_normal.png".format(list_elem))
        i.set_image_by_state(ButtonState.HOVERED, "res_placeholder{0}_hover.png".format(list_elem))
        i.add_action({ButtonEventType.ON_HOVER_ON: lambda: self.show_hint(r.locale_desc)})
        i.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.stop_hint()})
        # click_rect = copy(i.get_rect())
        # click_rect.x += self.resource_list_view.position[0] + 9
        # click_rect.y += self.resource_list_view.position[1]
        # i.set_click_rect(click_rect)
        # print(click_rect)
        self.resource_list_view.add_item(i)
        r_label.set_position(
            (r_label.position[0] + 14, r_label.position[1] + i.get_size()[1] / 2 - r_label.get_size()[1] / 2))
        amount_label.set_position(
            (i.position[0] + i.get_size()[0] - amount_label.get_size()[0] - 28, r_label.position[1]))

    def destroy(self) -> None:
        self.parent.remove_drawable(self.parent.find_drawable_by_type(PopupNotify))
        self.parent.remove_drawable(self)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
        self.close_btn.draw(screen)
        self.title_label.draw(screen)
        self.resource_list_view.draw(screen)
        self.name_res_label.draw(screen)
        self.amount_res_label.draw(screen)

    def handle_event(self, event) -> None:
        self.close_btn.handle_event(event)
        self.resource_list_view.handle_event(event)
