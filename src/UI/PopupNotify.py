import pygame
from src.Interfaces.Drawable import Drawable
from src.Scenes import Scene


class PopupNotify(Drawable):
    def __init__(self, parent: Scene, position: (int, int) = (0, 0), time_to_kill: int = 3) -> None:
        Drawable.__init__(self, parent, position)
        self.bg_image = pygame.image.load("../res/images/popup1.png").convert_alpha()
        self._rect.width = self.bg_image.get_rect().width
        self._rect.height = self.bg_image.get_rect().height
        self.__font = pygame.font.Font("../res/fonts/18480.ttf", 16)
        self.__time_to_kill = time_to_kill
        self.__start_time = pygame.time.get_ticks()
        self.text = ""
        self.text_image = None
        self.text_rect = None

        # self.close_btn = Button()
        # self.close_btn.rect.x = self.rect.topright[0] - 28
        # self.close_btn.rect.y = self.rect.topright[1] - 10

    def __del__(self):
        print("Destroy Popup")

    def set_text(self, text: str) -> None:
        self.text = text
        self.text_image = self.__font.render(self.text, True, (164, 107, 60))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = self.position[0] + 10
        self.text_rect.y = self.position[1] + 15

    def show(self) -> None:
        for p in self.parent.drawable_list:
            if type(p) is PopupNotify:
                p.destroy()
        self.parent.drawable_list.append(self)

    def destroy(self) -> None:
        if self in self.parent.drawable_list:
            self.parent.drawable_list.remove(self)

    def handle_event(self, event) -> None:
        pass
        # self.close_btn.handle_event(event)

    def update(self, dt) -> None:
        mills = (pygame.time.get_ticks() - self.__start_time) / 1000
        print(mills)
        if mills >= self.__time_to_kill:
            self.destroy()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg_image, self._rect)
        # self.close_btn.draw(screen)
        screen.blit(self.text_image, self.text_rect)
