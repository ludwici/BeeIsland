from copy import copy

import pygame

from src.Interfaces.RenderObject import RenderObject
from src.UI.ListItem import ListItem


class ListView(RenderObject):
    __slots__ = ("_data", "_item_padding", "padding", "bg_image", "_items_pos", "_item_distance")

    def __init__(self, parent, position: (int, int), size: (int, int), padding: (int, int) = (0, 0),
                 item_padding: (int, int) = (0, 0), item_distance: (int, int) = (0, 0)) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        self._data = []
        self._item_padding = item_padding
        self._item_distance = item_distance
        self.padding = padding
        self.bg_image = None
        self._rect.width = size[0]
        self._rect.height = size[1]
        self._items_pos = (self.position[0] + self.padding[0] + self._item_distance[0],
                           self.position[1] + self.padding[1] + self._item_distance[1])
        self.set_position(position)

    @property
    def item_padding(self) -> (int, int):
        return self._item_padding

    @item_padding.setter
    def item_padding(self, value: (int, int)):
        self._item_padding = value
        self._redraw_list()

    def index_of_value(self, i: ListItem):
        return self._data.index(i)

    def get_data(self) -> list:
        return copy(self._data)

    def set_image(self, path: str) -> None:
        self.bg_image = pygame.image.load(path).convert_alpha()

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self._items_pos = (self.position[0] + self.padding[0] + self._item_distance[0],
                           self.position[1] + self.padding[1] + self._item_distance[1])
        self._redraw_list()

    # def generate_list_items(self, item_template: ListItem):
    #     for s in self.source:
    #         i = item_template.copy()
    #         i.data = s
    #         self.add_item(i)
    #     self._redraw_list()

    def _redraw_list(self) -> None:
        self._items_pos = (self.position[0] + self.padding[0] + self._item_distance[0],
                           self.position[1] + self.padding[1] + self._item_distance[1])
        for i in self._data:
            self._set_item_position(i)
            self._items_pos = i.position[0] + i.size[0] + self._item_distance[0], self._items_pos[1]

    def _set_item_position(self, item: ListItem):
        value = item.size[0] + self._items_pos[0] + self._item_distance[0] - self.position[0]
        if len(self._data) != 1:
            if value > self.size[0]:
                self._items_pos = self.position[0] + self.padding[0] + self._item_distance[0], \
                                  self._items_pos[1] + item.size[1] + self._item_distance[1]
        item.set_position(position=self._items_pos, padding=self.item_padding)

    def add_item(self, item: ListItem) -> None:
        if len(self._data) > 0:
            last = self._data[-1]
            self._items_pos = (last.position[0] + last.size[0] + self._item_distance[0], self._items_pos[1])
        self._data.append(item)
        self._set_item_position(item)

    def remove_item(self, item: ListItem) -> None:
        self._data.remove(item)
        self._redraw_list()

    def handle_event(self, event) -> None:
        [d.handle_event(event) for d in self._data]

    def draw(self, screen: pygame.Surface) -> None:
        if self.bg_image:
            screen.blit(self.bg_image, self._rect)
        [d.draw(screen) for d in self._data if isinstance(d, RenderObject)]
