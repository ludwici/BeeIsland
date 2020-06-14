import pygame
from pygame.event import Event

from src.Quests.Quest import Quest, QuestDifficult
from src.Scenes.Beenix.Area import Area
from src.Scenes.Beenix.Beenix import Beenix, Direction
from src.Scenes.Beenix.Spider import Spider
from src.Scenes.QuestScene import QuestScene


class BeenixScene(QuestScene):
    __slots__ = ("__percent_zone", "__spider_count", "__area", "__area_surface", "__spiders", "__lives", "__beenix",
                 "__current_bee_index",)

    def __init__(self, main_window, name, player, quest: Quest) -> None:
        QuestScene.__init__(self, main_window=main_window, player=player, name=name, quest=quest)
        self.__percent_zone = 60 + 15 * int(self._quest.difficult == QuestDifficult.HARD)
        self.__spider_count = 2 + int(self._quest.difficult == QuestDifficult.HARD)
        self.__area = Area()
        self.__area_surface = self.__area.mask.count()
        self.__area.update_mask()
        self.__spiders = []
        self.__lives = len(self._quest.bee_list) + 1
        self.__current_bee_index = 0
        self.__beenix = Beenix(parent=self, area=self.__area, position=self.__area.rect.topleft)
        if len(self._quest.bee_list) != 0:
            self.__beenix.speed = self._quest.bee_list[self.__current_bee_index].speed
        else:
            self.__beenix.speed = 2

        for i in range(self.__spider_count):
            self.__spiders.append(Spider(self.__area))

    def __check_collisions(self) -> None:
        if self.__beenix.is_self_destruct():
            return self.wasted()
        for s in self.__spiders:
            if s.alive and s.on_line(self.__beenix.points) or self.__beenix.get_rect().colliderect(s.rect):
                return self.wasted()

    def on_scene_started(self) -> None:
        super().on_scene_started()
        self._timer_label.set_text(text=self._localization.get_string("time"))
        self._score_label.set_text(text=self._localization.get_string("score"))
        self._score_val_label.set_text(text="0")
        self._timer_label.set_position((10, self.__area.size[1] + 10))
        self._timer_val_label.set_position(
            (self._timer_label.position[0] + self._timer_label.size[0] + 10, self._timer_label.position[1]))

        self._score_label.set_position(
            (10, self._timer_label.size[1] + self._timer_label.position[1] - 10))
        self._score_val_label.set_position(
            (self._score_label.position[0] + self._score_label.size[0] + 10, self._score_label.position[1]))

        self._finish_button.set_text(text=self._localization.get_string("finish_label"))
        self._finish_button.set_padding(padding=(self._localization.get_params_by_string("finish_label")["x_off"], 0))
        self._finish_button.set_position((self._score_label.position[0],
                                          self._score_label.size[1] + self._score_label.position[1]))

    def handle_events(self, event: Event) -> None:
        super().handle_events(event)
        self.__beenix.handle_events(event)

    def __is_win(self) -> bool:
        return self.__percentage() > self.__percent_zone

    def update(self, dt: float) -> None:
        super().update(dt)
        self.__check_collisions()
        self.__beenix.update(self.__spiders)
        [s.update() for s in self.__spiders]
        rounded = round(self.__percentage(), 1)
        self._score_val_label.set_text(str("{0}/{1}".format(rounded, self.__percent_zone)))

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self.__area.draw(surface)
        self.__beenix.draw(surface)
        [s.draw(surface) for s in self.__spiders]

    def __percentage(self) -> float:
        return float(self.__area.mask.count() - self.__area_surface) / (
                self.__area.rect.w * self.__area.rect.h - self.__area_surface) * 100

    def wasted(self) -> None:
        self.__lives -= 1
        if self.__lives == 0:
            self._finish_quest()
            return

        if self.__lives == 1:
            speed = 3
        else:
            self.__current_bee_index += 1
            speed = self._quest.bee_list[self.__current_bee_index].speed

        self.__beenix = Beenix(parent=self, area=self.__area, position=self.__area.rect.topleft)
        self.__beenix.speed = speed
        self.__beenix.change_movement(Direction.STILL)
        pygame.time.delay(1000)
