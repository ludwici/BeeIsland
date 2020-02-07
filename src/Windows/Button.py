import pygame
from src.Interfaces.Drawable import Drawable


class Button(Drawable):
    def __init__(self, parent, path_to_image: str, text: str = "", position: (int, int) = (0, 0)) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self.image = None
        self.setImage(path_to_image)
        # self.bg_image_hovered = pygame.image.load("").convert_alpha()

        self.text = text
        self.hovered = False

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self._rect)

    def setImage(self, path: str) -> None:
        self.image = pygame.image.load(path).convert_alpha()
        self._rect.width = self.image.get_rect().width
        self._rect.height = self.image.get_rect().height

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self._rect.collidepoint(event.pos)

        # if self.hovered:
        #     self.image = self.bg_image_hovered
        # else:
        #     self.image = self.bg_image
