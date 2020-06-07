import math
from abc import abstractmethod

import pygame
from pygame.event import Event

from src.Database.Localization import Localization
from src.Quests.Quest import Quest
from src.Scenes.Scene import Scene
from src.UI.Button import ButtonState, ButtonEventType
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class QuestScene(Scene):
    __slots__ = ("_bg_image", "_quest", "_sec_to_finish", "_start_time", "_timer_label", "_timer_val_label",
                 "_time_over", "_score_label", "_score_val_label", "_finish_button", "score")

    def __init__(self, main_window, name, player, quest: Quest) -> None:
        Scene.__init__(self, main_window=main_window, name=name, player=player)
        self._bg_image = pygame.image.load("{0}/images/{1}_bg.png".format(self._res_dir, name)).convert_alpha()
        self._quest = quest
        self._sec_to_finish = 60 + self._quest.time - len(self._quest.bee_list) * 5
        self._start_time = 0
        self.score = 0
        self._timer_label = TextLabel(parent=self, font_size=32, color=(255, 255, 255))
        self._timer_val_label = TextLabel(parent=self, font_size=32, color=(255, 255, 255))
        self._time_over = False
        self._score_label = TextLabel(parent=self, font_size=32, color=(255, 255, 255))
        self._score_val_label = TextLabel(parent=self, font_size=32, color=(255, 255, 255))
        finish_label = TextLabel(parent=self, font_size=24)
        self._finish_button = TextButton(parent=self, text_label=finish_label,
                                         normal_image_path="start_quest_btn_normal.png")
        self._finish_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")
        self._finish_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self._finish_quest()})

    @abstractmethod
    def _time_over_handle(self) -> None:
        pass

    @staticmethod
    def __diff(bee_lvl: int):
        if bee_lvl <= 1:
            return 0
        elif bee_lvl == 2:
            return 1
        elif bee_lvl == 3:
            return 3
        else:
            return 6

    def __mxp(self, bee_lvl: int):
        if self._quest.zone == 1:
            mod = 5
        elif self._quest.zone == 2:
            mod = 25
        elif self._quest.zone == 3:
            mod = 65
        else:
            mod = 205
        return mod + (2 * bee_lvl)

    @staticmethod
    def rf(bee_lvl):
        if bee_lvl == 1:
            return 1
        elif bee_lvl <= 2 or bee_lvl <= 4:
            return 1 - (bee_lvl - 10) / 100
        elif bee_lvl == 5:
            return 0.82
        else:
            return 1

    def _calculate_xp(self, bee_lvl: int):
        xp = math.ceil(((8 * bee_lvl) + QuestScene.__diff(bee_lvl)) * self.__mxp(bee_lvl) * QuestScene.rf(bee_lvl))
        return xp

    @staticmethod
    def _calculate_damage():
        return 16

    def _finish_quest(self) -> None:
        self.player.resources += self._quest.rewards
        self.player.resources += self._quest.additional_rewards
        for b in self._quest.bee_list:
            b.give_xp(self._calculate_xp(b.current_level))
            b.current_hp -= QuestScene._calculate_damage()
        self.score += self.score * self._quest.score_modifier_percent / 100

        self.main_window.prev_scene.complete_quest(self._quest.quest_id)
        self.main_window.change_scene(self.main_window.prev_scene.name)
        self.main_window.remove_scene(self.name)

    def update(self, dt: float) -> None:
        super().update(dt)

        if self._time_over:
            return
        self._sec_to_finish -= (1 * dt) / 1000
        if self._sec_to_finish > 0:
            self._timer_val_label.set_text(str(int(self._sec_to_finish)))
        else:
            self._time_over = True
            self._time_over_handle()

    def on_scene_started(self) -> None:
        self._localization = Localization(path="scenes/Quest")
        self._start_time = pygame.time.get_ticks()

    def handle_events(self, event: Event) -> None:
        self._finish_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        surface.blit(self._bg_image, self._bg_image.get_rect())
        self._timer_label.draw(surface)
        self._timer_val_label.draw(surface)
        self._score_label.draw(surface)
        self._score_val_label.draw(surface)
        self._finish_button.draw(surface)
