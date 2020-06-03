import pygame
from pygame.event import Event

import Constants
from Interfaces.Drawable import Drawable
from Scenes.Scene import Scene
from UI.Button import Button, ButtonState, ButtonEventType
from UI.TextLabel import TextLabel


class Menu(Drawable):
    __slots__ = ("_close_btn", "_bg_image", "_title_label")

    def __init__(self, parent: Scene, bg_name):
        Drawable.__init__(self, parent=parent)
        self.parent.remove_drawable(self.parent.find_child_of(child=self, base=Menu))
        self._close_btn = Button(parent=self, normal_image_path="close_button1.png")
        self._close_btn.set_image_by_state(ButtonState.HOVERED, "close_button1_hover.png")
        self._close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})

        self._bg_image = pygame.image.load("{0}/{1}.png".format(self._res_dir, bg_name)).convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height
        position = (Constants.WINDOW_W / 2 - self._bg_image.get_rect().width / 2, 70)
        self.set_position(position)
        self._close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

        self._title_label = TextLabel(parent=self, position=self.position, font_size=16, bold=True)

        self.parent.add_drawable(self)

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self._close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

    def destroy(self):
        self.parent.remove_drawable(self)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
        self._close_btn.draw(screen)
        self._title_label.draw(screen)

    def handle_event(self, event: Event) -> None:
        self._close_btn.handle_event(event)
