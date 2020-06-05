import pygame
from pygame.event import Event

from src import Constants
from src.Database.Database import Database
from src.Quests.Quest import Quest
from src.Scenes.Map.MapZone import MapZone
from src.Scenes.Map.QuestMenu import QuestMenu
from src.Scenes.Scene import Scene
from src.UI.Button import Button, ButtonState, ButtonEventType
from src.UI.PopupNotify import PopupNotify


class MapScene(Scene):
    __slots__ = ("__map_image", "__bg_map_rect", "zones", "to_farm_button", "__bg_image", "__bg_rect")

    def __init__(self, main_window, name, player) -> None:
        Scene.__init__(self, main_window=main_window, player=player, name=name)
        self.__bg_image = pygame.image.load("{0}/images/map1_bg.jpg".format(self._res_dir))
        self.__bg_rect = self.__bg_image.get_rect()
        self.__map_image = pygame.image.load("{0}/images/map1.jpg".format(self._res_dir)).convert()
        self.__bg_map_rect = self.__map_image.get_rect()
        self.zones = []
        self.to_farm_button = Button(parent=self, position=(10, 10), normal_image_path="to_farm_normal.png")
        self.to_farm_button.set_image_by_state(ButtonState.HOVERED, "to_farm_hover.png")
        self.to_farm_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.change_scene("Farm")})

    def on_scene_started(self) -> None:
        super().on_scene_started()
        self.__bg_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)
        self.__bg_map_rect.center = (Constants.WINDOW_W / 2, Constants.WINDOW_H / 2)
        self.init_zones()

    def show_quest_menu(self, quest) -> None:
        QuestMenu(parent=self, quest=quest)

    def init_zones(self) -> None:
        bg_x, bg_y = self.__bg_map_rect.x, self.__bg_map_rect.y
        zone1 = MapZone(self, "zone1", position=(bg_x + 20, bg_y + 75))
        zone2 = MapZone(self, "zone2", position=(bg_x + 83, bg_y + 375))
        zone3 = MapZone(self, "zone3", position=(bg_x + 488, bg_y + 183))
        zone4 = MapZone(self, "zone4", position=(bg_x + 298, bg_y + 33))
        zone5 = MapZone(self, "zone5", position=(bg_x + 415, bg_y + 465))
        zone6 = MapZone(self, "zone6", position=(bg_x + 285, bg_y + 214))
        zone7 = MapZone(self, "zone7", position=(bg_x + 383, bg_y + 578))
        zone1.unlock()

        db = Database.get_instance()
        quest_data = db.get_all_quests()
        for qd in quest_data:
            quest = Quest(quest_template=qd, icon_offset=(bg_x, bg_y))
            zone1.add_quest(quest)

        self.zones.extend([zone1, zone2, zone3, zone4, zone5, zone6, zone7])

    def on_scene_change(self) -> None:
        super().on_scene_change()
        self.zones.clear()

    def handle_events(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space")

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for z in self.zones:
                    if z.get_rect().collidepoint(event.pos):
                        if z.is_locked and z.can_handle_events:
                            PopupNotify(parent=self, text=self.localization.get_string("locked_zone"))

        [z.handle_event(event) for z in self.zones]
        [d.handle_event(event) for d in self._drawable_list]
        self.to_farm_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((38, 34, 35))
        surface.blit(self.__map_image, self.__bg_map_rect)
        [z.draw(surface) for z in self.zones]
        super().draw(surface)
        self.to_farm_button.draw(surface)
