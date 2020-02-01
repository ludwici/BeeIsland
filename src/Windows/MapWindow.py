import pygame
from pygame.rect import Rect

from src.MapZone import MapZone
from src.Windows.PopupNotify import PopupNotify
from src.Windows.RenderWindow import RenderWindow


class MapWindow(RenderWindow):
    def __init__(self, width=761, height=761) -> None:
        RenderWindow.__init__(self, width, height)
        self.bg_image = pygame.image.load("../res/images/map1.jpg").convert()
        self.zones = []
        self.drawable_list = []
        self.initZones()

    def showPopup(self, position, text) -> None:
        p = PopupNotify()
        p.rect = position
        if text:
            p.setText(text)
        self.drawable_list.append(p)

    def initZones(self) -> None:
        zone1 = MapZone("Zone1", pos_x=20, pos_y=75)
        zone2 = MapZone("Zone2", pos_x=83, pos_y=375)
        zone3 = MapZone("Zone3", pos_x=488, pos_y=183)
        zone4 = MapZone("Zone4", pos_x=298, pos_y=33)
        zone5 = MapZone("Zone5", pos_x=415, pos_y=465)
        zone6 = MapZone("Zone6", pos_x=285, pos_y=214)
        zone7 = MapZone("Zone7", pos_x=383, pos_y=578, has_fog=False)

        zone1.unlock()

        self.zones.append(zone1)
        self.zones.append(zone2)
        self.zones.append(zone3)
        self.zones.append(zone4)
        self.zones.append(zone5)
        self.zones.append(zone6)
        self.zones.append(zone7)

    def loop(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for z in self.zones:
                        if z.show_border:
                            z.onClick(self)
                            break

            for z in self.zones:
                if z.click_rect.collidepoint(pygame.mouse.get_pos()):
                    z.onMouseOver()
                else:
                    z.onMouseOut()

        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image, self.bg_image.get_rect())
        for z in self.zones:
            z.draw(self.screen)

        for d in self.drawable_list:
            d.draw(self.screen)

        pygame.display.flip()
        return False
