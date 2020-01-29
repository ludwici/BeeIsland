import pygame

from src.Windows.RenderWindow import RenderWindow


class MapWindow(RenderWindow):
    def __init__(self, width=761, height=761):
        RenderWindow.__init__(self, width, height)
        self.bg_image = pygame.image.load("../res/images/map1.jpg")

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image, self.bg_image.get_rect())
        pygame.display.flip()
        return False
