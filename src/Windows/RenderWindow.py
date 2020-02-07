import os
import pygame

from abc import ABC, abstractmethod
from src.Windows.PopupNotify import PopupNotify
from pygame.time import Clock


class RenderWindow(ABC):
    def __init__(self, width=640, height=480) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.size = self.width, self.height = width, height
        self.bg_color = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Bee Island")
        self.__popup = PopupNotify(parent=self)
        self.drawable_list = []
        self.clock = Clock()

    def start(self) -> None:
        while self.loop():
            pass
        pygame.quit()
        quit()

    def showPopup(self, position, text) -> None:
        if self.__popup in self.drawable_list:
            self.drawable_list.remove(self.__popup)

        self.__popup = PopupNotify(parent=self, position=position)
        if text:
            self.__popup.setText(text)
        self.__popup.show()

    @abstractmethod
    def loop(self) -> bool:
        return True
