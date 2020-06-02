import pygame
from pygame.event import Event

from src import Constants
from src.Quests.Quest import Quest
from src.Scenes.Beenix.Area import Area
from src.Scenes.Beenix.Beenix import Beenix, Direction
from src.Scenes.Beenix.Spider import Spider
from src.Scenes.QuestScene import QuestScene


class BeenixScene(QuestScene):

    def __init__(self, main_window, name, player, quest: Quest) -> None:
        QuestScene.__init__(self, main_window=main_window, player=player, name=name, quest=quest)
        self._percent_zone = 60
        self._spider_count = 2
        self._area = Area()
        self._area_surface = self._area.mask.count()
        self._area.update_mask()
        self._spiders = []
        self._beenix = Beenix(parent=self, area=self._area, position=self._area.rect.topleft)
        for i in range(self._spider_count):
            self._spiders.append(Spider(self._area))

    def _time_over_handle(self) -> None:
        pass

    def check_collisions(self) -> None:
        if self._beenix.is_self_destruct():
            return self.wasted()
        for s in self._spiders:
            if s.alive and s.on_line(self._beenix.points) or self._beenix.get_rect().colliderect(s.rect):
                return self.wasted()

    def on_scene_started(self) -> None:
        super().on_scene_started()
        self._timer_label.set_text(text=self._localization.get_string("time"))
        self._score_label.set_text(text=self._localization.get_string("score"))
        self._score_val_label.set_text(text="0")
        self._timer_label.set_position((10, self._area.size[1] + 10))
        self._timer_val_label.set_position(
            (self._timer_label.position[0] + self._timer_label.get_size()[0] + 10, self._timer_label.position[1]))

        self._score_label.set_position(
            (10, self._timer_label.get_size()[1] + self._timer_label.position[1] - 10))
        self._score_val_label.set_position(
            (self._score_label.position[0] + self._score_label.get_size()[0] + 10, self._score_label.position[1]))

        self._finish_button.set_text(text=self._localization.get_string("finish_label"))
        self._finish_button.set_padding(padding=(self._localization.get_params_by_string("finish_label")["x_off"], 0))
        self._finish_button.set_position((Constants.WINDOW_W - self._finish_button.get_size()[0] - 10, 10))

    def handle_events(self, event: Event) -> None:
        super().handle_events(event)
        self._beenix.handle_events(event)

    def is_win(self) -> bool:
        return self.percentage() > self._percent_zone

    def update(self, dt: float) -> None:
        super().update(dt)
        self.check_collisions()
        self._beenix.update(self._spiders)
        [s.update() for s in self._spiders]

        self._score_val_label.set_text(str("{0:.1f}".format(self.percentage()) + '%'))

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self._area.draw(surface)
        self._beenix.draw(surface)
        [s.draw(surface) for s in self._spiders]

    def percentage(self) -> float:
        return float(self._area.mask.count() - self._area_surface) / (
                    self._area.rect.w * self._area.rect.h - self._area_surface) * 100

    def wasted(self) -> None:
        self._beenix = Beenix(parent=self, area=self._area, position=self._area.rect.topleft)
        self._beenix.change_movement(Direction.STILL)
        pygame.time.delay(1000)
