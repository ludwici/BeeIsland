from threading import Thread

from src.Interfaces.Drawable import *


class PopupNotify(Drawable):
    def __init__(self, parent: RenderWindow, position=Rect((0, 0, 0, 0))) -> None:
        Drawable.__init__(self, parent, position)
        self.bg_image = pygame.image.load("../res/images/popup1.png").convert_alpha()
        self.rect.width = self.bg_image.get_rect().width
        self.rect.height = self.bg_image.get_rect().height
        self.time = 3000
        self.start_ticks = pygame.time.get_ticks()
        self.__font = pygame.font.Font("../res/fonts/18480.ttf", 16)
        self.text = ""
        self.text_image = None
        self.text_rect = None

        self.color = (255, 255, 255)
        self.__destroy_thread = Thread(target=self.__destroy, daemon=True)
        # self.close_btn = Button()
        # self.close_btn.rect.x = self.rect.topright[0] - 28
        # self.close_btn.rect.y = self.rect.topright[1] - 10

    def __del__(self):
        print("Destroy")

    def setText(self, text: str) -> None:
        self.text = text
        self.text_image = self.__font.render(self.text, True, (164, 107, 60))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = self.rect.x + 10
        self.text_rect.y = self.rect.y + 15

    def __destroy(self):
        while True:
            milliseconds = pygame.time.get_ticks() - self.start_ticks
            if milliseconds >= self.time:
                self.destroy()
                break

    def destroy(self):
        if self in self.parent.drawable_list:
            self.parent.drawable_list.remove(self)

    def show(self):
        if self not in self.parent.drawable_list:
            self.parent.drawable_list.append(self)
            self.__destroy_thread.start()

    def handle_event(self, event) -> None:
        pass
        # self.close_btn.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg_image, self.rect)
        # self.close_btn.draw(screen)
        if self.text:
            screen.blit(self.text_image, self.text_rect)
