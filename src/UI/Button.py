import pygame
from typing import Callable
from src.Interfaces.Drawable import Drawable


class Button(Drawable):
    def __init__(self, parent, path_to_image: str, text: str = "", position: (int, int) = (0, 0)) -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self.image = None
        self.setImage(path_to_image)
        self.action_list = []
        self.text = text
        self.hovered = False

    def update(self, dt) -> None:
        pass

    def addAction(self, action: Callable) -> None:
        self.action_list.append(action)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self._rect)

    def setImage(self, path: str) -> None:
        self.image = pygame.image.load(path).convert_alpha()
        self._rect.width = self.image.get_rect().width
        self._rect.height = self.image.get_rect().height

    def onClick(self) -> None:
        [a() for a in self.action_list]

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self._rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if event.button == 1:
                self.onClick()

        # if self.hovered:
        #     self.image = self.bg_image_hovered
        # else:
        #     self.image = self.bg_image
