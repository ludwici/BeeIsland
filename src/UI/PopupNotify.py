import pygame

from src.Interfaces.Drawable import Drawable
from src.Timer import Timer


class PopupNotify(Drawable):
    def __init__(self, parent, position: (int, int) = (0, 0)) -> None:
        Drawable.__init__(self, parent, position)
        self.bg_image = pygame.image.load("../res/images/popup1.png").convert_alpha()
        self._rect.width = self.bg_image.get_rect().width
        self._rect.height = self.bg_image.get_rect().height
        self.__font = pygame.font.Font("../res/fonts/18480.ttf", 16)
        self.timer = Timer(mills=3000)
        self.timer.after_times_actions.append(self.destroy)
        self.text = ""
        self.text_image = None
        self.text_rect = None

        # self.close_btn = Button()
        # self.close_btn.rect.x = self.rect.topright[0] - 28
        # self.close_btn.rect.y = self.rect.topright[1] - 10

    def __del__(self):
        print("Destroy Popup")

    def setText(self, text: str) -> None:
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
        self.parent.timer_list.append(self.timer)
        self.timer.start()

    def destroy(self) -> None:
        if self in self.parent.drawable_list:
            self.parent.drawable_list.remove(self)

    def handle_event(self, event) -> None:
        pass
        # self.close_btn.handle_event(event)

    def update(self, dt) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg_image, self._rect)
        # self.close_btn.draw(screen)
        screen.blit(self.text_image, self.text_rect)
