import pygame
from src.Scenes.Scene import Scene


class Match3Scene(Scene):
    def __init__(self, main_window) -> None:
        Scene.__init__(self, main_window=main_window)
        self.bg_image = pygame.image.load("../res/images/quest_bg1.png").convert_alpha()

    def update(self, dt) -> None:
        pass

    def handle_events(self, event) -> None:
        pass

    def draw(self, surface) -> None:
        surface.blit(self.bg_image, self.bg_image.get_rect())
