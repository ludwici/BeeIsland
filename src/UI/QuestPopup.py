import pygame
from pygame.event import Event

from src.UI.Button import Button
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.PopupNotify import PopupNotify
from src.Scenes import Scene
from src.UI.TextLabel import TextLabel


class QuestPopup(PopupNotify):
    count = 0

    def __init__(self, parent: Scene, position: (int, int), text: str = "") -> None:
        self.close_btn = Button(parent=self, path_to_image="../res/images/close_button1.png",
                                hovered_image="../res/images/close_button1_hover.png")
        PopupNotify.__init__(self, parent=parent, position=position)
        self.close_btn.set_position(position=(0, 0))
        self.close_btn.add_action(lambda: self.destroy())
        self._time_to_kill = 0

        self.rewards_text = text

        self.set_background("../res/images/popup3.png")
        position.x = self.parent.main_window.width / 2 - self.bg_rect.width / 2
        self.set_position(position)
        self.quest_label = TextLabel(parent=self, text="Title", position=self.position, font_name="segoeprint",
                                     font_size=16, bold=True, color=(159, 80, 17))
        self.description_label = MultilineTextLabel(parent=self, text="description", position=position,
                                                    font_name="segoeprint", font_size=14, color=(159, 80, 17),
                                                    line_length=self.bg_rect.width - 35 * 2)
        self.difficult_label = TextLabel(parent=self, text="difficult", position=position, font_name="segoeprint",
                                         font_size=14, color=(159, 80, 17))

    @classmethod
    def create(cls, scene: Scene, position: (int, int), *args, **kwargs) -> "QuestPopup":
        if QuestPopup.count == 0:
            q = cls(parent=scene, position=position)
            q.show()
        else:
            q = scene.find_drawable_by_type(QuestPopup)
            position.x = q.parent.main_window.width / 2 - q.bg_rect.width / 2
            q.set_position(position)
        quest_data = kwargs["quest"]
        q.quest_label.set_text(quest_data.title)
        q.quest_label.set_position(
            (q.position[0] + q.bg_rect.centerx - q.quest_label.get_size()[0] / 2, q.position[1] + 3)
        )
        q.description_label.set_position((q.position[0] + 35, q.position[1] + 74))
        q.description_label.set_text(quest_data.description)
        q.difficult_label.set_text("Уровень сложности")
        q.difficult_label.set_position((q.position[0] + q.bg_rect.centerx - q.difficult_label.get_size()[0] / 2,
                                        q.description_label.position[1] + q.description_label.get_size()[1] + 60))

        return q

    def show(self) -> None:
        QuestPopup.count += 1
        super().show()

    def destroy(self) -> None:
        QuestPopup.count -= 1
        super().destroy()

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.close_btn.draw(screen)
        self.quest_label.draw(screen)
        self.description_label.draw(screen)
        self.difficult_label.draw(screen)

    def handle_event(self, event: Event) -> None:
        self.close_btn.handle_event(event)
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            for z in self.parent.zones:
                z.on_mouse_out()
