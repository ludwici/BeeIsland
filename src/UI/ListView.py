from copy import copy

import pygame

from src.Interfaces.Drawable import Drawable
from src.UI.ListItem import ListItem


class ListView(Drawable):
    def __init__(self, parent, position: (int, int), padding: (int, int) = (0, 0),
                 item_padding: (int, int) = (15, 15)) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self._data = []
        self._item_padding = item_padding
        self.padding = padding
        self.bg_image = None
        self._items_pos = self.position + self.padding
        self.set_position(position)

    @property
    def item_padding(self) -> (int, int):
        return copy(self._item_padding)

    @item_padding.setter
    def item_padding(self, value: (int, int)):
        self._item_padding = value
        self._redraw_list()

    def get_data(self) -> list:
        return copy(self._data)

    def set_image(self, path: str) -> None:
        self.bg_image = pygame.image.load(path).convert_alpha()
        self._rect.width = self.bg_image.get_rect().width
        self._rect.height = self.bg_image.get_rect().height

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self._items_pos = self.position[0] + self.padding[0], self.position[1] + self.padding[1]
        self._redraw_list()

    def _redraw_list(self) -> None:
        self._items_pos = self.position[0] + self.padding[0], self.position[1] + self.padding[1]
        for i in self._data:
            self._set_item_position(i)
            self._items_pos = i.position[0] + i.get_size()[0] + self.item_padding[0], self._items_pos[1]

    def _set_item_position(self, item: ListItem):
        value = item.get_size()[0] + self._items_pos[0] + self.item_padding[0] - self.position[0]
        if value > self.get_size()[0]:
            self._items_pos = self.position[0] + self.padding[0], \
                              self._items_pos[1] + item.get_size()[1] + self.item_padding[1]
        item.set_position(self._items_pos)

    def add_item(self, item: ListItem) -> None:
        if len(self._data) > 0:
            last = self._data[-1]
            self._items_pos = last.position[0] + last.get_size()[0] + self.item_padding[0], self._items_pos[1]
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
        [d.draw(screen) for d in self._data if isinstance(d, Drawable)]
