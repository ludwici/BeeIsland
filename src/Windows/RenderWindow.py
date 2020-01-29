from abc import ABC, abstractmethod
import os
import pygame


class RenderWindow(ABC):
    def __init__(self, width=640, height=480):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.size = self.width, self.height = width, height
        self.bg_color = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)

    @abstractmethod
    def loop(self):
        pass
