import os
import pygame

from src.Scenes.MapScene import MapScene
from pygame.time import Clock


class RenderWindow:
    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Bee Island")
        self.size = self.width, self.height = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.bg_color = 0, 0, 0
        self.bg_image = pygame.image.load("../res/images/map1.jpg").convert()
        self.current_scene = MapScene(self)
        self.done = False
        self.clock = Clock()

    def start(self) -> None:
        while not self.done:
            self.loop()
        pygame.quit()
        quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.current_scene.handle_events(event)

    def loop(self) -> None:
        dt = self.clock.tick(60)
        self.handle_events()
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image, self.bg_image.get_rect())
        self.current_scene.update(dt)
        self.current_scene.draw(surface=self.screen)
        pygame.display.flip()

