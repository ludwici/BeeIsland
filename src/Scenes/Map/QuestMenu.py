import pygame
from pygame.event import Event

from src import Constants
from src.BeeFamily.Bee import Bee
from src.Interfaces.Drawable import Drawable
from src.QuestSettings import QuestSettings, QuestDifficult
from src.Quests.Questable import Questable
from src.UI.BeeSelectPanel import BeeSelectPanel
from src.UI.BeeSocket import BeeSocket
from src.UI.Button import Button, ButtonState, ButtonEventType
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class QuestMenu(Drawable):
    __slots__ = ("close_btn", "quest", "_bg_image", "quest_settings", "panel_rect", "quest_label", "description_label",
                 "difficult_label", "rewards_label", "easy_button", "medium_button", "hard_button", "rewards_panel",
                 "bonuses_panel", "bonuses_rect", "bonus_list", "bee_socket_group", "bee_socket_hard", "start_button",
                 "rewards_labels", "rewards_rect")

    def __init__(self, parent, quest: Questable) -> None:
        Drawable.__init__(self, parent=parent)
        self.close_btn = Button(parent=self, normal_image_path="close_button1.png")
        self.close_btn.set_image_by_state(ButtonState.HOVERED, "close_button1_hover.png")
        self.close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})
        self.quest = quest
        self._bg_image = pygame.image.load("{0}/popup3.png".format(self._res_dir)).convert_alpha()
        self._rect.width = self._bg_image.get_rect().width
        self._rect.height = self._bg_image.get_rect().height
        position = (Constants.WINDOW_W / 2 - self._bg_image.get_rect().width / 2, 70)
        self.set_position(position)
        self.quest_settings = QuestSettings()
        self.panel_rect = pygame.Rect((self.position[0] + 15, self.position[1] + 155, self.get_size()[0] - 15 * 2, 277))

        self.quest_label = TextLabel(parent=self, text=self.quest.title, position=self.position, font_size=16,
                                     bold=True)
        self.quest_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self.quest_label.get_size()[0] / 2,
             self.position[1] + 3)
        )
        ll = self._bg_image.get_rect().width - self.parent.localization.get_params_by_string("desc_label")[
            "line_length"] * 2 - 35
        self.description_label = MultilineTextLabel(parent=self, text=self.quest.description, line_length=ll,
                                                    position=(self.position[0] + 35, self.position[1] + 75),
                                                    font_size=14)
        self.difficult_label = TextLabel(parent=self, text=self.parent.localization.get_string("difficult_label"),
                                         position=(position[0], self.panel_rect.y + 10), font_size=14)

        self.rewards_label = TextLabel(parent=self, text=self.parent.localization.get_string("reward_label"),
                                       position=position, font_size=14, )

        easy_label = TextLabel(parent=self, text=self.parent.localization.get_string("easy"), font_size=14)
        self.easy_button = TextButton(parent=self, normal_image_path="difficult/easy_normal.png",
                                      text_label=easy_label, text_padding=(19, 0))
        self.easy_button.set_position(
            (self.position[0] + 35, self.difficult_label.position[1] + self.difficult_label.get_size()[1] + 9)
        )
        self.easy_button.set_image_by_state(ButtonState.HOVERED, "difficult/easy_hovered.png")

        medium_label = TextLabel(parent=self, text=self.parent.localization.get_string("medium"), font_size=14,
                                 color=(138, 36, 12))
        self.medium_button = TextButton(parent=self,
                                        normal_image_path="difficult/medium_normal.png",
                                        text_label=medium_label, text_padding=(19, 0))
        self.medium_button.set_position(
            (self.easy_button.position[0], self.easy_button.position[1] + self.easy_button.get_size()[1])
        )
        self.medium_button.set_image_by_state(ButtonState.HOVERED,
                                              "difficult/medium_hovered.png")

        hard_label = TextLabel(parent=self, text=self.parent.localization.get_string("hard"), font_size=14,
                               color=(159, 17, 17))
        self.hard_button = TextButton(parent=self, normal_image_path="difficult/hard_normal.png",
                                      text_label=hard_label, text_padding=(19, 0))
        self.hard_button.set_position(
            (self.medium_button.position[0], self.medium_button.position[1] + self.medium_button.get_size()[1])
        )
        self.hard_button.set_image_by_state(ButtonState.HOVERED, "difficult/hard_hovered.png")

        self.rewards_panel = pygame.image.load("{0}/rewards_list_bg.png".format(self._res_dir))

        self.bonuses_panel = pygame.image.load(
            "{0}/buttons/difficult/bonuses.png".format(self._res_dir)).convert_alpha()
        self.bonuses_rect = self.bonuses_panel.get_rect()
        self.bonuses_rect.x = self.easy_button.position[0] + self.easy_button.get_size()[0]
        self.bonuses_rect.y = self.easy_button.position[1]

        self.difficult_label.set_position(
            (self.easy_button.position[0] + (self.easy_button.get_size()[0] + self.bonuses_rect.width) / 2
             - self.difficult_label.get_size()[0] / 2, self.difficult_label.position[1])
        )

        self.bonus_list = []

        self.rewards_rect = self.rewards_panel.get_rect()

        bs_start_y = self.bonuses_rect.y
        self.bee_socket_group = RadioGroup()
        all_bees = self.parent.player.farm.bees_from_all_hives
        for i in range(3):
            b = BeeSocket(parent=self, normal_image_path="socket1_normal.png",
                          group=self.bee_socket_group,
                          position=(self.bonuses_rect.x + self.bonuses_rect.width + 46, bs_start_y))
            b.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
            b.show_select_panel(self, all_bees)
            b.remove(self)
            bs_start_y += b.get_size()[1] + 8

        self.bee_socket_hard = BeeSocket(parent=self, normal_image_path="socket2_normal.png",
                                         group=self.bee_socket_group, state=ButtonState.LOCKED,
                                         position=(self.bonuses_rect.x + self.bonuses_rect.width + 46, bs_start_y + 15))
        self.bee_socket_hard.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
        self.bee_socket_hard.set_image_by_state(ButtonState.LOCKED, "socket3_normal.png")

        self.bee_socket_hard.show_select_panel(self, all_bees)
        self.bee_socket_hard.remove(self)

        start_label = TextLabel(parent=self, text=self.parent.localization.get_string("start_button"), position=(0, 0),
                                font_size=24)
        self.start_button = TextButton(parent=self, text_label=start_label, text_padding=(
            self.parent.localization.get_params_by_string("start_button")["x_off"], 0),
                                       normal_image_path="start_quest_btn_normal.png", )
        self.start_button.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self.start_button.get_size()[0] / 2,
             self.panel_rect.y + self.panel_rect.height + 33)
        )
        self.start_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")

        self.rewards_labels = []

        self.rewards_rect.x = self.position[0] + 35
        self.rewards_rect.y = self.bonuses_rect.y + self.bonuses_rect.height + 41

        self.rewards_label.set_position(
            (self.rewards_rect.centerx - self.rewards_label.get_size()[0] / 2,
             self.bonuses_rect.y + self.bonuses_rect.height + 8)
        )

        self.easy_button.add_action(
            {ButtonEventType.ON_CLICK_LB: lambda d=QuestDifficult.EASY: self.change_difficult(d)}
        )
        self.medium_button.add_action(
            {ButtonEventType.ON_CLICK_LB: lambda d=QuestDifficult.MEDIUM: self.change_difficult(d)}
        )
        self.hard_button.add_action(
            {ButtonEventType.ON_CLICK_LB: lambda d=QuestDifficult.HARD: self.change_difficult(d)}
        )
        self.start_button.add_action(
            {ButtonEventType.ON_CLICK_LB: lambda: self.parent.main_window.change_scene("Match3", self.quest_settings)}
        )

        self.change_difficult(QuestDifficult.EASY)

    def add_bee_to_socket(self, b: Bee):
        b.setup_bonus(self.quest)

    def generate_bonuses_labels(self) -> None:
        start_pos_y = self.bonuses_rect.y
        self.bonus_list.clear()
        for bs in self.bee_socket_group.buttons:
            if bs.bee:
                b_l = MultilineTextLabel(parent=self, text=bs.bee.bonus, bold=True, line_length=130, font_size=12,
                                         position=(self.bonuses_rect.x + 5, start_pos_y))
                self.bonus_list.append(b_l)
                start_pos_y += b_l.get_size()[1]
        self.generate_rewards_labels()

    def generate_rewards_labels(self) -> None:
        self.rewards_labels.clear()
        pos_x = self.rewards_rect.x + 20
        pos_y = self.rewards_rect.y + 10
        for r in self.quest.rewards.get_bag_copy():
            r_l = TextLabel(parent=self, text="{0}: {1}".format(r.locale_name, int(r.value)), bold=True, font_size=12)
            r_l.set_position((pos_x, pos_y))
            pos_y += r_l.get_size()[1] - 5
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

        self.bee_socket_hard.lock() if difficult != QuestDifficult.HARD else self.bee_socket_hard.unlock()

        self.rewards_labels.clear()
        self.generate_rewards_labels()

    def destroy(self) -> None:
        self.parent.remove_drawable(self.parent.find_drawable_by_type(BeeSelectPanel))
        self.parent.remove_drawable(self)

    def set_position(self, position: (int, int)) -> None:
        super().set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg_image, self._rect)
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
        self.rewards_label.draw(screen)
        screen.blit(self.bonuses_panel, self.bonuses_rect)
        [b_l.draw(screen) for b_l in self.bonus_list]
        self.bee_socket_group.draw(screen)

    def update(self, dt: float) -> None:
        self.generate_bonuses_labels()

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
