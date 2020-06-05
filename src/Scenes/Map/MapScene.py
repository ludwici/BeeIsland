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
    __slots__ = ("__map_image", "__bg_map_rect", "zones", "to_farm_button", "__bg_image", "__bg_rect",
                 "__unlocked_zones", "__completed_quests")

    def __init__(self, main_window, name, player) -> None:
        Scene.__init__(self, main_window=main_window, player=player, name=name)
        self.__bg_image = pygame.image.load("{0}/images/map1_bg.jpg".format(self._res_dir))
        self.__bg_rect = self.__bg_image.get_rect()
        self.__map_image = pygame.image.load("{0}/images/map1.jpg".format(self._res_dir)).convert()
        self.__bg_map_rect = self.__map_image.get_rect()
        self.zones = []
        self.__unlocked_zones = set()
        self.__unlocked_zones.add(1)
        self.__completed_quests = set()
        self.__completed_quests.add(1)
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
        positions = [(bg_x + 20, bg_y + 75), (bg_x + 83, bg_y + 375), (bg_x + 488, bg_y + 183), (bg_x + 298, bg_y + 33),
                     (bg_x + 415, bg_y + 465), (bg_x + 285, bg_y + 214), (bg_x + 383, bg_y + 578)]

        for i in range(7):
            zone = MapZone(self, i + 1, position=(positions[i][0], positions[i][1]))
            self.zones.append(zone)

        db = Database.get_instance()
        quest_data = db.get_all_quests()

        for qd in quest_data:
            quest = Quest(quest_template=qd, icon_offset=(bg_x, bg_y))
            available = quest.quest_id in self.__completed_quests
            self.zones[quest.zone - 1].add_quest(quest, available)

        [z.lock() for z in self.zones]
        for i in self.__unlocked_zones:
            self.zones[i - 1].unlock()

    def on_scene_change(self) -> None:
        super().on_scene_change()
        self.zones.clear()

    def complete_quest(self, quest_id: int):
        self.__completed_quests.add(quest_id + 1)
        if quest_id == 4:
            self.__unlocked_zones.add(2)
        elif quest_id == 6:
            self.__unlocked_zones.add(3)

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
        [r.handle_event(event) for r in self._render_list]
        self.to_farm_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((38, 34, 35))
        surface.blit(self.__map_image, self.__bg_map_rect)
        [z.draw(surface) for z in self.zones]
        super().draw(surface)
        self.to_farm_button.draw(surface)
