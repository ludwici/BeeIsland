import pygame
from pygame.event import Event

from src.UI.Button import Button
from src.UI.PopupNotify import PopupNotify
from src.Scenes import Scene


class QuestPopup(PopupNotify):
    count = 0

    def __init__(self, parent: Scene, position: (int, int), text: str = ""):
        self.close_btn = Button(parent=self, path_to_image="../res/images/close_button1.png")
        PopupNotify.__init__(self, parent=parent, position=position)
        self.close_btn.set_position(position=(0, 0))
        self.close_btn.add_action(lambda: self.destroy())
        self._time_to_kill = 0

        self.rewards_text = text

        self.set_background("../res/images/popup3.png")
        position.x = self.parent.main_window.width / 2 - self.bg_rect.width / 2
        self.set_position(position)

    @classmethod
    def create(cls, scene: Scene, position: (int, int), text: str) -> "QuestPopup":
        if QuestPopup.count == 0:
            q = cls(parent=scene, position=position, text=text)
            q.show()
            QuestPopup.count += 1
        else:
            q = scene.find_drawable_by_type(QuestPopup)
            position.x = q.parent.main_window.width / 2 - q.bg_rect.width / 2
            q.set_position(position)
            q.set_text(q.text)
        return q

    def destroy(self) -> None:
        QuestPopup.count -= 1
        super().destroy()

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.close_btn.draw(screen)

    def handle_event(self, event: Event) -> None:
        self.close_btn.handle_event(event)
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            for z in self.parent.zones:
                z.on_mouse_out()
