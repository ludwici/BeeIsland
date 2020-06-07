import pygame

from src.UI.Button import Button


class ListItem(Button):
    __slots__ = ("data", "__center")

    def __init__(self, parent, normal_image_path: str, data=None, center: bool = False) -> None:
        Button.__init__(self, parent=parent, normal_image_path=normal_image_path)
        self.data = data
        self.__center = center

    # def copy(self):
    #     cls = self.__class__
    #     cls_list = inspect.getmro(cls)[:-1]
    #     result = cls.__new__(cls)
    #
    #     for c in cls_list:
    #         slots = c.__slots__
    #         if not isinstance(slots, tuple):
    #             slots = tuple((slots,))
    #         for var in slots:
    #             setattr(result, var, copy.copy(getattr(self, var)))
    #
    #     for a in self._action_list:
    #         print(a.__code__.co_argcount)
    #
    #     return result

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if self.data:
            self.data.handle_event(event)

    def set_position(self, position: (int, int), padding: (int, int) = (0, 0)) -> None:
        super().set_position(position)
        if self.data:
            if not self.__center:
                self.data.set_position((position[0] + padding[0], position[1] + padding[1]))
            else:
                self.data.get_rect().center = self._rect.center

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.data:
            self.data.draw(screen)
