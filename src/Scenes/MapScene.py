import pygame

from src.MapZone import MapZone
from src.Quests.Match3 import Match3
from src.Scenes.Scene import Scene


class MapScene(Scene):
    def __init__(self, main_window) -> None:
        Scene.__init__(self, main_window=main_window)
        self.zones = []
        self.initZones()

    def initZones(self) -> None:
        zone1 = MapZone(self, "Zone1", pos_x=20, pos_y=75)
        zone2 = MapZone(self, "Zone2", pos_x=83, pos_y=375)
        zone3 = MapZone(self, "Zone3", pos_x=488, pos_y=183)
        zone4 = MapZone(self, "Zone4", pos_x=298, pos_y=33)
        zone5 = MapZone(self, "Zone5", pos_x=415, pos_y=465)
        zone6 = MapZone(self, "Zone6", pos_x=285, pos_y=214)
        zone7 = MapZone(self, "Zone7", pos_x=383, pos_y=578, has_fog=False)

        q1 = Match3(zone=zone1, icon_position=(110, 120))
        q1.condition = True
        q1.check_allow()

        q2 = Match3(zone=zone1, icon_position=(90, 160))
        q2.condition = True
        q2.check_allow()

        zone1.unlock()

        self.zones.extend([zone1, zone2, zone3, zone4, zone5, zone6, zone7])

    def handle_events(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for z in self.zones:
                    if z.show_border:
                        z.onClick()
                        break

        for z in self.zones:
            if z.click_rect.collidepoint(pygame.mouse.get_pos()):
                z.onMouseOver()
            else:
                z.onMouseOut()

        [d.handle_event(event) for d in self.drawable_list]

    def draw(self, surface) -> None:
        for z in self.zones:
            z.draw(surface)

        for d in self.drawable_list:
            d.draw(surface)

    def update(self, dt) -> None:
        self.check_timers()