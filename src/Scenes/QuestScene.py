import pygame
from pygame.event import Event

from Database.Localization import Localization
from Quests.Questable import Questable
from Scenes.Scene import Scene
from UI.Button import ButtonState, ButtonEventType
from UI.TextButton import TextButton
from UI.TextLabel import TextLabel
from abc import abstractmethod


class QuestScene(Scene):
    __slots__ = ("_bg_image", "_quest", "_sec_to_finish", "_start_time", "_timer_label", "_timer_val_label",
                 "_time_over", "_score_label", "_score_val_label", "_finish_button")

    def __init__(self, main_window, name, player, quest: Questable) -> None:
        Scene.__init__(self, main_window=main_window, name=name, player=player)
        self._bg_image = pygame.image.load("{0}/images/{1}_bg.png".format(self._res_dir, name)).convert_alpha()
        self._quest = quest
        self._sec_to_finish = 60 + self._quest.time
        self._start_time = 0
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

    def _finish_quest(self) -> None:
        self.player.resources += self._quest.rewards
        self.player.resources += self._quest.additional_rewards
        # TODO: give XP to bees

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
