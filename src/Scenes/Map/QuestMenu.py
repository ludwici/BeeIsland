import pygame
from pygame.event import Event

from UI.Menu import Menu
from src.BeeFamily.Bee import Bee
from src.Quests.Quest import Quest, QuestDifficult
from src.Scenes.Beenix.BeenixScene import BeenixScene
from src.Scenes.Match3.Match3Scene import Match3Scene
from src.UI.BeeSelectPanel import BeeSelectPanel
from src.UI.BeeSocket import BeeSocket, BeeSocketType
from src.UI.Button import ButtonState, ButtonEventType
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class QuestMenu(Menu):
    __slots__ = ("quest", "quest_settings", "panel_rect", "description_label",
                 "difficult_label", "rewards_label", "easy_button", "medium_button", "hard_button", "rewards_panel",
                 "bonuses_panel", "bonuses_rect", "bonus_list", "bee_socket_group", "bee_socket_hard", "start_button",
                 "rewards_labels", "rewards_rect")

    def __init__(self, parent, quest: Quest) -> None:
        Menu.__init__(self, parent=parent, bg_name="popup3")
        self.quest = quest
        self._title_label.set_text(text=self.quest.title)
        self._title_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self._title_label.get_size()[0] / 2 + 10,
             self.position[1] + 3)
        )

        self.panel_rect = pygame.Rect((self.position[0] + 15, self.position[1] + 155, self.get_size()[0] - 15 * 2, 277))

        ll = self._bg_image.get_rect().width - self.parent.localization.get_params_by_string("desc_label")[
            "line_length"] * 2 - 35
        self.description_label = MultilineTextLabel(parent=self, text=self.quest.description, line_length=ll,
                                                    position=(self.position[0] + 35, self.position[1] + 75),
                                                    font_size=14)
        self.difficult_label = TextLabel(parent=self, text=self.parent.localization.get_string("difficult_label"),
                                         position=(self.position[0], self.panel_rect.y + 10), font_size=14)

        self.rewards_label = TextLabel(parent=self, text=self.parent.localization.get_string("reward_label"),
                                       position=self.position, font_size=14, )

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
            b = BeeSocket(parent=self, can_change_id=False,
                          group=self.bee_socket_group, socket_type=BeeSocketType.WORKER,
                          position=(self.bonuses_rect.x + self.bonuses_rect.width + 46, bs_start_y))
            b.show_select_panel(self, all_bees)
            b.remove(self)
            bs_start_y += b.get_size()[1] + 8

        self.bee_socket_hard = BeeSocket(parent=self,
                                         socket_type=BeeSocketType.WARRIOR, group=self.bee_socket_group,
                                         state=ButtonState.LOCKED, can_change_id=False,
                                         position=(self.bonuses_rect.x + self.bonuses_rect.width + 46, bs_start_y + 15))
        self.bee_socket_hard.set_image_by_state(ButtonState.LOCKED, "socket3_normal.png")

        self.bee_socket_hard.show_select_panel(self, all_bees)

        start_label = TextLabel(parent=self, text=self.parent.localization.get_string("start_button"), position=(0, 0),
                                font_size=24)
        self.start_button = TextButton(parent=self, text_label=start_label, text_padding=(
            self.parent.localization.get_params_by_string("start_button")["x_off"], 0),
                                       normal_image_path="start_quest_btn_normal.png")
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
            {ButtonEventType.ON_CLICK_LB: lambda: self.start_quest()}
        )

        self.change_difficult(QuestDifficult.EASY)

        for z in self.parent.zones:
            z.stop_handle()

    def start_quest(self) -> None:
        bee_list = []
        for b in self.bee_socket_group.buttons:
            if b.bee:
                bee_list.append(b.bee)
                print("Q" + repr(b.bee))

        self.quest.bee_list = bee_list
        if self.quest.q_type == 1:
            q = Match3Scene(main_window=self.parent.main_window, name="Match3", player=self.parent.player,
                            quest=self.quest)
        elif self.quest.q_type == 4:
            q = BeenixScene(main_window=self.parent.main_window, name="Beenix", player=self.parent.player,
                            quest=self.quest)
        else:
            q = Match3Scene(main_window=self.parent.main_window, name="Match3", player=self.parent.player,
                            quest=self.quest)

        self.parent.add_scene(scene_name=q.name, scene=q)
        self.parent.change_scene(q.name)

    def remove_bee_from_socket(self, socket) -> None:
        socket.bee.remove_bonus(self.quest)
        self.change_difficult(self.quest.difficult)

    def add_bee_to_socket(self, b: Bee) -> None:
        b.setup_bonus(self.quest)
        self.change_difficult(self.quest.difficult)

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
        self.quest.difficult = difficult
        bag = self.quest.rewards.get_bag_copy()
        if difficult == QuestDifficult.EASY:
            percent = self.quest.resources_modifier * 0
        elif difficult == QuestDifficult.MEDIUM:
            percent = self.quest.resources_modifier + 15
        else:
            percent = self.quest.resources_modifier + 35

        for r in bag:
            r.increase_by_percent(percent)

        self.bee_socket_hard.lock() if difficult != QuestDifficult.HARD else self.bee_socket_hard.unlock()

        self.rewards_labels.clear()
        self.generate_rewards_labels()

    def destroy(self) -> None:
        for z in self.parent.zones:
            z.start_handle()
        self.parent.remove_drawable(self.parent.find_drawable_by_type(BeeSelectPanel))
        super().destroy()

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        pygame.draw.rect(screen, (24, 15, 7), self.panel_rect)
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
        super().handle_event(event)
        self.easy_button.handle_event(event)
        self.medium_button.handle_event(event)
        self.hard_button.handle_event(event)
        self.start_button.handle_event(event)
        self.bee_socket_group.handle_event(event)
