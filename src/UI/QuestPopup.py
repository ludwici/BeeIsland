import pygame
from pygame.event import Event

from src import Constants
from src.BeeSocket import BeeSocket
from src.QuestSettings import QuestSettings, QuestDifficult
from src.Scenes import Scene
from src.UI.Button import Button
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class QuestPopup(PopupNotify):
    count = 0

    def __init__(self, parent: Scene) -> None:
        self.close_btn = Button(parent=self, path_to_image="../res/images/buttons/close_button1.png",
                                hovered_image="../res/images/buttons/close_button1_hover.png")
        PopupNotify.__init__(self, parent=parent)
        self.close_btn.set_position(position=(0, 0))
        self.close_btn.add_action(lambda: self.destroy())
        self._time_to_kill = 0
        self.quest = None

        self.set_background("../res/images/popup3.png")
        position = (Constants.WINDOW_W / 2 - self.bg_rect.width / 2, 70)
        self.set_position(position)
        self.quest_settings = QuestSettings()
        self.quest_label = TextLabel(parent=self, text="Title", position=self.position, font_name="segoeprint",
                                     font_size=16, bold=True, color=(159, 80, 17))
        self.description_label = MultilineTextLabel(parent=self, text="description", position=position,
                                                    font_name="segoeprint", font_size=14, color=(159, 80, 17),
                                                    line_length=self.bg_rect.width - 35 * 2)
        self.panel_rect = pygame.Rect((self.position[0] + 15, self.position[1], self.get_size()[0] - 15 * 2, 277))
        self.difficult_label = TextLabel(parent=self, text="Уровень сложности", position=position,
                                         font_name="segoeprint", font_size=14, color=(159, 80, 17))
        self.bonus_label = TextLabel(parent=self, text="Бонусы", position=position, font_name="segoeprint",
                                     font_size=14, color=(159, 80, 17))

        easy_label = TextLabel(parent=self, text="Лёгкий", position=(0, 0), font_name="segoeprint", font_size=14,
                               color=(159, 80, 17))
        self.easy_button = TextButton(parent=self, path_to_image="../res/images/buttons/difficult/easy_normal.png",
                                      hovered_image="../res/images/buttons/difficult/easy_hover.png",
                                      text_label=easy_label, text_padding=(19, 0))
        medium_label = TextLabel(parent=self, text="Средний", position=(0, 0), font_name="segoeprint", font_size=14,
                                 color=(138, 36, 12))
        self.medium_button = TextButton(parent=self, path_to_image="../res/images/buttons/difficult/medium_normal.png",
                                        hovered_image="../res/images/buttons/difficult/medium_hover.png",
                                        text_label=medium_label, text_padding=(19, 0))
        hard_label = TextLabel(parent=self, text="Сложный", position=(0, 0), font_name="segoeprint", font_size=14,
                               color=(159, 17, 17))
        self.hard_button = TextButton(parent=self, path_to_image="../res/images/buttons/difficult/hard_normal.png",
                                      hovered_image="../res/images/buttons/difficult/hard_hover.png",
                                      text_label=hard_label, text_padding=(19, 0))
        self.rewards_panel = pygame.image.load("../res/images/buttons/difficult/rewards.png").convert_alpha()
        self.bonus_panel = pygame.image.load("../res/images/bonus_list_bg.png")
        self.rewards_rect = self.rewards_panel.get_rect()
        self.bonus_rect = self.bonus_panel.get_rect()

        self.bee_socket_group = RadioGroup()
        for i in range(3):
            BeeSocket(parent=self, path_to_image="../res/images/buttons/socket1_normal.png",
                      group=self.bee_socket_group, selected_image="../res/images/buttons/socket1_normal.png",
                      position=(0, 0))

        self.bee_socket_hard = BeeSocket(parent=self, path_to_image="../res/images/buttons/socket2_normal.png",
                                         group=self.bee_socket_group, is_locked=True,
                                         selected_image="../res/images/buttons/socket2_normal.png", position=(0, 0))

        start_label = TextLabel(parent=self, text="Начать", position=(0, 0), font_name="segoeprint", font_size=24,
                                color=(159, 80, 17))
        self.start_button = TextButton(parent=self, path_to_image="../res/images/buttons/start_quest_btn.png",
                                       text_label=start_label, text_padding=(44, 0))

        self.rewards_labels = []

        self.easy_button.add_action(lambda d=QuestDifficult.EASY: self.change_difficult(d))
        self.medium_button.add_action(lambda d=QuestDifficult.MEDIUM: self.change_difficult(d))
        self.hard_button.add_action(lambda d=QuestDifficult.HARD: self.change_difficult(d))
        self.start_button.add_action(
            lambda name="Match3", s=self.quest_settings: self.parent.main_window.change_scene(scene_name=name,
                                                                                              settings=s)
        )

    @classmethod
    def create(cls, scene: Scene, *args, **kwargs) -> "QuestPopup":
        if QuestPopup.count == 0:
            q = cls(parent=scene)
            q.show()
        else:
            q = scene.find_drawable_by_type(QuestPopup)
            q.set_position((Constants.WINDOW_W / 2 - q.bg_rect.width / 2, 70))
        q.quest = kwargs["quest"]
        q.quest_label.set_text(q.quest.title)
        q.quest_label.set_position(
            (q.position[0] + q.bg_rect.centerx - q.quest_label.get_size()[0] / 2, q.position[1] + 3)
        )
        q.description_label.set_position((q.position[0] + 35, q.position[1] + 74))
        q.description_label.set_text(q.quest.description)
        q.panel_rect.y = q.description_label.position[1] + q.description_label.get_size()[1] + 45
        q.difficult_label.set_position(
            (q.position[0] + q.bg_rect.centerx - q.difficult_label.get_size()[0] / 2, q.panel_rect.y + 8)
        )
        q.easy_button.set_position(
            (q.position[0] + 35, q.difficult_label.position[1] + q.difficult_label.get_size()[1] + 9)
        )
        q.medium_button.set_position(
            (q.easy_button.position[0], q.easy_button.position[1] + q.easy_button.get_size()[1])
        )
        q.hard_button.set_position(
            (q.medium_button.position[0], q.medium_button.position[1] + q.medium_button.get_size()[1])
        )
        q.start_button.set_position(
            (q.position[0] + q.bg_rect.centerx - q.start_button.get_size()[0] / 2,
             q.panel_rect.y + q.panel_rect.height + 40)
        )
        q.rewards_rect.x = q.easy_button.position[0] + q.easy_button.get_size()[0]
        q.rewards_rect.y = q.easy_button.position[1]

        bs_start_y = q.rewards_rect.y
        for bs in q.bee_socket_group.buttons[:-1]:
            bs.set_position(
                (q.rewards_rect.x + q.rewards_rect.width + 46, bs_start_y)
            )
            bs_start_y += bs.get_size()[1] + 8

        q.bee_socket_hard.set_position(
            (q.rewards_rect.x + q.rewards_rect.width + 46, bs_start_y + 15)
        )

        q.generate_reward_labels((q.rewards_rect.x + 33, q.rewards_rect.y))

        q.bonus_label.set_position(
            (q.position[0] + q.bg_rect.centerx - q.bonus_label.get_size()[0] / 2,
             q.rewards_rect.y + q.rewards_rect.height + 8)
        )

        q.bonus_rect.x = q.position[0] + 35
        q.bonus_rect.y = q.bonus_label.position[1] + q.bonus_label.get_size()[1] + 9

        q.change_difficult(QuestDifficult.EASY)
        return q

    def generate_reward_labels(self, start_pos: (int, int)) -> None:
        pos_y = start_pos[1]
        for r in self.quest.rewards.get_bag_copy():
            r_l = TextLabel(parent=self, text="{0}: {1}".format(r.locale_name, int(r.value)), position=(0, 0),
                            font_name="segoeprint", font_size=12, color=(159, 80, 17))
            r_l.set_position((start_pos[0], pos_y))
            pos_y += r_l.get_size()[1]
            self.rewards_labels.append(r_l)

    def change_difficult(self, difficult: QuestDifficult) -> None:
        self.quest_settings.set_difficult(difficult)
        bag = self.quest.rewards.get_bag_copy()
        for r in bag:
            if difficult == QuestDifficult.EASY:
                r.increaseByPercent(0)
            elif difficult == QuestDifficult.MEDIUM:
                r.increaseByPercent(15)
            elif difficult == QuestDifficult.HARD:
                r.increaseByPercent(35)

        self.bee_socket_hard.is_locked = not difficult == QuestDifficult.HARD

        self.rewards_labels.clear()
        self.generate_reward_labels((self.rewards_rect.x + 33, self.rewards_rect.y))

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
        pygame.draw.rect(screen, (24, 15, 7), self.panel_rect)
        self.close_btn.draw(screen)
        self.quest_label.draw(screen)
        self.description_label.draw(screen)
        self.difficult_label.draw(screen)
        self.easy_button.draw(screen)
        self.medium_button.draw(screen)
        self.hard_button.draw(screen)
        self.start_button.draw(screen)
        screen.blit(self.rewards_panel, self.rewards_rect)
        [r_l.draw(screen) for r_l in self.rewards_labels]
        self.bonus_label.draw(screen)
        screen.blit(self.bonus_panel, self.bonus_rect)
        self.bee_socket_group.draw(screen)

    def handle_event(self, event: Event) -> None:
        self.close_btn.handle_event(event)
        self.easy_button.handle_event(event)
        self.medium_button.handle_event(event)
        self.hard_button.handle_event(event)
        self.start_button.handle_event(event)
        self.bee_socket_group.handle_event(event)
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            for z in self.parent.zones:
                z.on_mouse_out()
