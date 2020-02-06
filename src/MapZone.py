import copy
import pygame
from src.Windows import MapWindow
from pygame.rect import Rect


class MapZone:
    def __init__(self, name, pos_x, pos_y, has_fog=True) -> None:
        self.name = name
        self.border_image = pygame.image.load("../res/images/zones/border_{0}.png".format(self.name)).convert_alpha()
        self.__is_lock = True
        self.zone_rect = self.border_image.get_rect()
        self.zone_rect.x = pos_x
        self.zone_rect.y = pos_y

        self.click_rect = copy.copy(self.zone_rect)
        self.click_rect.height -= 30
        self.click_rect.width -= 50
        self.click_rect.x += 35

        self.has_fog = has_fog
        self.show_border = False
        self.fog_rect = None
        try:
            self.fog_image = pygame.image.load("../res/images/zones/fog_{0}.png".format(self.name)).convert_alpha()
            self.fog_rect = self.fog_image.get_rect()
            self.fog_rect.center = self.zone_rect.center
        except pygame.error:
            self.has_fog = False

    @property
    def is_lock(self) -> bool:
        return self.__is_lock

    def unlock(self) -> None:
        self.__is_lock = False
        self.has_fog = False

    def onMouseOver(self) -> None:
        self.show_border = True

    def onMouseOut(self) -> None:
        self.show_border = False

    def onClick(self, map_window: MapWindow) -> None:
        if self.is_lock:
            mouse_pos = pygame.mouse.get_pos()
            popup_pos = [0, 0]
            if mouse_pos[0] + 200 + 20 > map_window.size[0]:
                popup_pos[0] = mouse_pos[0] - 200
            else:
                popup_pos[0] = mouse_pos[0]

            popup_pos[1] = mouse_pos[1] - 70
            if popup_pos[1] < 0:
                popup_pos[1] += 70

            position = Rect(popup_pos[0], popup_pos[1], 200, 70)
            map_window.showPopup(position, "Эта зона ещё не открыта")

    def draw(self, screen: pygame.Surface) -> None:
        if self.show_border:
            screen.blit(self.border_image, self.zone_rect)
        if self.has_fog:
            screen.blit(self.fog_image, self.fog_rect)
