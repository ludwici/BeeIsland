import pygame

from pygame.event import Event
from src.Scenes.Scene import Scene


class Match3Scene(Scene):
    def __init__(self, main_window) -> None:
        Scene.__init__(self, main_window=main_window)
        self.bg_image = pygame.image.load("../res/images/quest_bg1.png").convert_alpha()

    def update(self, dt: float) -> None:
        pass

    def handle_events(self, event: Event) -> None:
        pass

    def on_scene_change(self) -> None:
        super().on_scene_change()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg_image, self.bg_image.get_rect())
