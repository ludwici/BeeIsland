import pygame

from pygame.event import Event
from src.Interfaces.Drawable import Drawable
from src.Scenes import Scene


class PopupNotify(Drawable):
    def __init__(self, parent: Scene, position: (int, int) = (0, 0), time_to_kill: int = 3, text: str = "") -> None:
        Drawable.__init__(self, parent=parent, position=position)
        self._bg_image = None
        self.set_background("../res/images/popup1.png")
        self.__font = pygame.font.Font("../res/fonts/18480.ttf", 16)
        self._time_to_kill = time_to_kill
        self.__start_time = pygame.time.get_ticks()
        self.text = text
        self.text_image = None
        self.text_rect = None
        self.set_text(text=text)

        # self.close_btn = Button()
        # self.close_btn.rect.x = self.rect.topright[0] - 28
        # self.close_btn.rect.y = self.rect.topright[1] - 10

    def __del__(self):
        print("Destroy Popup")

    def set_background(self, path_to_image: str) -> None:
        self._bg_image = pygame.image.load(path_to_image).convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height

    @classmethod
    def create(cls, scene: Scene, position: (int, int), text: str) -> "PopupNotify":
        p = cls(parent=scene, position=position, text=text)
        p.show()
        return p

    def set_text(self, text: str) -> None:
        if not text:
            return
        self.text_image = self.__font.render(self.text, True, (164, 107, 60))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = self.position[0] + 10
        self.text_rect.y = self.position[1] + 15

    def show(self) -> None:
        self.parent.add_drawable(self)

    def destroy(self) -> None:
        self.parent.remove_drawable(self)

    def handle_event(self, event: Event) -> None:
        pass
        # self.close_btn.handle_event(event)

    def update(self, dt: float) -> None:
        if self._time_to_kill != 0:
            mills = (pygame.time.get_ticks() - self.__start_time) / 1000
            if mills >= self._time_to_kill:
                self.destroy()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
        # self.close_btn.draw(screen)
        if self.text:
            screen.blit(self.text_image, self.text_rect)
