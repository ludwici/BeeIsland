import pygame
from pygame.event import Event

from src import Constants
from src.BeeSocket import BeeSocket
from src.Scenes.Scene import Scene
from src.UI.Button import Button
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class ModifyPopup(PopupNotify):
    count = 0

    def __init__(self, parent: Scene) -> None:
        self.close_btn = Button(parent=self, path_to_image="../res/images/buttons/close_button1.png",
                                hovered_image="../res/images/buttons/close_button1_hover.png")
        PopupNotify.__init__(self, parent=parent)
        self.close_btn.set_position(position=(0, 0))
        self.close_btn.add_action(lambda: self.destroy())
        self._time_to_kill = 0
        self.set_background("../res/images/modify_popup1.png")
        position = (Constants.WINDOW_W / 2 - self.bg_rect.width / 2, 70)
        self.set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

        self.title_label = TextLabel(parent=self, text="Улучшение", position=self.position, font_name="segoeprint",
                                     font_size=16, bold=True, color=(159, 80, 17))
        self.socket_group = RadioGroup()
        self.socket1 = BeeSocket(parent=self, path_to_image="../res/images/buttons/socket1_normal.png",
                                 group=self.socket_group, selected_image="../res/images/buttons/socket5_normal.png",
                                 position=(0, 0))
        self.socket2 = BeeSocket(parent=self, path_to_image="../res/images/buttons/socket1_normal.png",
                                 group=self.socket_group, selected_image="../res/images/buttons/socket5_normal.png",
                                 position=(0, 0))
        self.result_socket = BeeSocket(parent=self, path_to_image="../res/images/buttons/socket1_normal.png",
                                       group=self.socket_group, is_locked=True,
                                       selected_image="../res/images/buttons/socket5_normal.png", position=(0, 0))
        upgrade_label = TextLabel(parent=self, text="Улучшить", position=(0, 0), font_name="segoeprint", font_size=18,
                                  color=(159, 80, 17))
        self.upgrade_button = TextButton(parent=self, path_to_image="../res/images/buttons/start_quest_btn.png",
                                         text_label=upgrade_label, text_padding=(40, 4))
        self.dna_image = pygame.image.load("../res/images/dna1.png").convert_alpha()
        self.dna_rect = self.dna_image.get_rect()
        self.info_block_image = pygame.image.load("../res/images/modify_popup1_info.png")
        self.info_block_rect = self.info_block_image.get_rect()
        self.info_text_label = TextLabel(parent=self, text="Информация", position=(0, 0), font_name="segoeprint",
                                         font_size=14, color=(159, 80, 17))

    @classmethod
    def create(cls, scene: Scene, *args, **kwargs) -> "ModifyPopup":
        if ModifyPopup.count == 0:
            m = cls(parent=scene)
            m.show()
        else:
            m = scene.find_drawable_by_type(ModifyPopup)
            m.set_position((Constants.WINDOW_W / 2 - m.bg_rect.width / 2, 70))

        m.title_label.set_position(
            (m.position[0] + m.bg_rect.centerx - m.title_label.get_size()[0] / 2 + 10, m.position[1] + 3)
        )

        m.socket1.set_position((m.position[0] + 102, m.position[1] + 135))
        m.dna_rect.x = m.socket1.position[0] + m.socket1.get_size()[1] + 12
        m.dna_rect.y = m.socket1.get_rect().centery - m.dna_rect.height / 2
        m.socket2.set_position((m.dna_rect.x + m.dna_rect.width + 7, m.socket1.position[1]))
        m.upgrade_button.set_position((m.socket1.position[0], m.socket2.position[1] + m.socket2.get_size()[1] + 15))
        m.result_socket.set_position(
            (m.upgrade_button.get_rect().centerx - m.result_socket.get_size()[1] / 2,
             m.upgrade_button.position[1] + m.upgrade_button.get_size()[1] + 15)
        )
        m.info_block_rect.x = m.upgrade_button.position[0] + m.upgrade_button.get_size()[0] + 95
        m.info_block_rect.y = m.position[1] + 71
        m.info_text_label.set_position(
            (m.info_block_rect.centerx - m.info_text_label.get_size()[0] / 2, m.info_block_rect.y)
        )

        return m

    def show(self) -> None:
        ModifyPopup.count += 1
        super().show()

    def destroy(self) -> None:
        ModifyPopup.count -= 1
        super().destroy()

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.close_btn.draw(screen)
        self.title_label.draw(screen)
        self.socket_group.draw(screen)
        self.upgrade_button.draw(screen)
        screen.blit(self.dna_image, self.dna_rect)
        screen.blit(self.info_block_image, self.info_block_rect)
        self.info_text_label.draw(screen)

    def handle_event(self, event: Event) -> None:
        self.close_btn.handle_event(event)
        self.socket_group.handle_event(event)
        self.upgrade_button.handle_event(event)
