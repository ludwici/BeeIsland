import pygame
from pygame.rect import Rect

from src.Interfaces.Drawable import Drawable


class Button(Drawable):
    def __init__(self, text: str = "", position=Rect((0, 0, 0, 0))) -> None:
        Drawable.__init__(self, position)
        self.bg_image = pygame.image.load("../res/images/exit_btn.png").convert_alpha()
        self.bg_image_hovered = pygame.image.load("../res/images/exit_btn_hovered.png").convert_alpha()

        self.image = self.bg_image

        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        self.text = text
        self.hovered = False

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if self.hovered:
            self.image = self.bg_image_hovered
        else:
            self.image = self.bg_image
