import pygame
from pygame.event import Event

from Database.Database import Database
from Scenes.Map.MapZone import MapZone
from src import Constants
from src.Quests.Match3 import Match3
from src.Scenes.Scene import Scene
from src.UI.Button import Button, ButtonState, ButtonEventType


class MapScene(Scene):
    def __init__(self, main_window, player) -> None:
        Scene.__init__(self, main_window=main_window, player=player)
        self.bg_image = pygame.image.load("../res/images/map1.jpg").convert()
        self.bg_image_rect = self.bg_image.get_rect()
        self.bg_image_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)
        self.zones = []
        self.to_farm_button = Button(parent=self, normal_image_path="../res/images/buttons/to_farm_normal.png")
        self.to_farm_button.set_image_by_state(ButtonState.HOVERED, "../res/images/buttons/to_farm_hover.png")
        self.to_farm_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.main_window.change_scene("Farm")})

    def on_scene_started(self) -> None:
        self.init_zones()

    def init_zones(self) -> None:
        bg_x = self.bg_image_rect.x
        bg_y = self.bg_image_rect.y
        zone1 = MapZone(self, "Zone1", pos_x=bg_x + 20, pos_y=bg_y + 75)
        zone2 = MapZone(self, "Zone2", pos_x=bg_x + 83, pos_y=bg_y + 375)
        zone3 = MapZone(self, "Zone3", pos_x=bg_x + 488, pos_y=bg_y + 183)
        zone4 = MapZone(self, "Zone4", pos_x=bg_x + 298, pos_y=bg_y + 33)
        zone5 = MapZone(self, "Zone5", pos_x=bg_x + 415, pos_y=bg_y + 465)
        zone6 = MapZone(self, "Zone6", pos_x=bg_x + 285, pos_y=bg_y + 214)
        zone7 = MapZone(self, "Zone7", pos_x=bg_x + 383, pos_y=bg_y + 578, has_fog=False)
        zone1.unlock()

        db = Database.get_instance()
        quest_data = db.get_all_quests()
        for qd in quest_data:
            quest = Match3(quest_template=qd, icon_offset=(bg_x, bg_y))
            zone1.add_quest(quest)

        self.zones.extend([zone1, zone2, zone3, zone4, zone5, zone6, zone7])

    def on_scene_change(self) -> None:
        super().on_scene_change()
        self.zones.clear()

    def handle_events(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for z in self.zones:
                    if z.show_border:
                        z.on_click()
                        break

        [z.handle_event(event) for z in self.zones]
        [d.handle_event(event) for d in self._drawable_list]
        self.to_farm_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((38, 34, 35))
        surface.blit(self.bg_image, self.bg_image_rect)
        [z.draw(surface) for z in self.zones]
        [d.draw(surface) for d in self._drawable_list]
        self.to_farm_button.draw(surface)

    def update(self, dt: float) -> None:
        [d.update(dt) for d in self._drawable_list]
