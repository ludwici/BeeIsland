import copy
import pygame


class MapZone:

    def __init__(self, name, pos_x, pos_y, has_fog=True) -> None:
        self.name = name
        self.border_image = pygame.image.load("../res/images/zones/border_{0}.png".format(self.name)).convert_alpha()

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
        except:
            self.has_fog = False

    def onMouseOver(self) -> None:
        self.show_border = True

    def onMouseOut(self) -> None:
        self.show_border = False

    def draw(self, screen: pygame.Surface) -> None:
        if self.show_border:
            screen.blit(self.border_image, self.zone_rect)
        if self.has_fog:
            screen.blit(self.fog_image, self.fog_rect)

