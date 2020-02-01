import pygame
from pygame.rect import Rect

from src.Interfaces.Drawable import Drawable
from src.Windows.Button import Button


class PopupNotify(Drawable):
    def __init__(self, position=Rect((0, 0, 0, 0))) -> None:
        Drawable.__init__(self, position)
        self.bg_image = pygame.image.load("../res/images/popup1.png").convert_alpha()
        self.rect.width = self.bg_image.get_rect().width
        self.rect.height = self.bg_image.get_rect().height
        self.time = 0

        self.__font = pygame.font.Font("freesansbold.ttf", 14)
        self.text = ""
        self.text_image = None
        self.text_rect = None

        self.color = (255, 255, 255)
        self.close_btn = Button()

    def setText(self, text: str) -> None:
        self.text = text
        self.text_image = self.__font.render(self.text, True, (164, 107, 60))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = self.rect.x + 10
        self.text_rect.y = self.rect.y + 15

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg_image, self.rect)
        if self.text:
            screen.blit(self.text_image, self.text_rect)
