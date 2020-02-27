import pygame
from pygame.event import Event

from src.UI.PopupNotify import PopupNotify
from src.Scenes import Scene


class QuestPopup(PopupNotify):
    count = 0

    def __init__(self, parent: Scene, position: (int, int), text: str = ""):
        PopupNotify.__init__(self, parent=parent, position=position, text=text)
        self._time_to_kill = 0
        self.set_background("../res/images/popup2.png")

    @classmethod
    def create(cls, scene: Scene, position: (int, int), text: str) -> "QuestPopup":
        if QuestPopup.count == 0:
            q = cls(parent=scene, position=position, text=text)
            q.show()
            QuestPopup.count += 1
        else:
            q = scene.find_drawable_by_type(QuestPopup)
            q.set_position(position)
            q.set_text(q.text)
        return q

    def handle_event(self, event: Event) -> None:
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            for z in self.parent.zones:
                z.on_mouse_out()
