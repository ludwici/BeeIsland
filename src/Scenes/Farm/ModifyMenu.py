import itertools
import math
import random

import pygame
from pygame.event import Event

from DNAEntity import DNAEntity
from Database.Database import Database
from src.BeeFamily.Bee import Bee
from src.BeeFamily.BeeQueen import BeeQueen
from src.BeeFamily.BeeWarrior import BeeWarrior
from src.BeeFamily.BeeWorker import BeeWorker
from src.Scenes.Scene import Scene
from src.UI.BeeSocket import BeeSocket, BeeSocketType
from src.UI.Button import ButtonEventType, ButtonState
from src.UI.ListItem import ListItem
from src.UI.ListView import ListView
from src.UI.Menu import Menu
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.RadioGroup import RadioGroup
from src.UI.RenderGroup import RenderGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class ModifyMenu(Menu):
    __slots__ = (
        "socket_group", "socket1", "socket2", "upgrade_button", "result_socket", "info_block_image", "info_block_rect",
        "info_text_label", "info_group", "bee_list_view", "dna_image", "dna_rect")

    def __init__(self, parent: Scene) -> None:
        Menu.__init__(self, parent=parent, bg_name="modify_popup1")
        self._title_label.set_text(text=self.parent.localization.get_string("modify_title"))
        self._title_label.set_position(
            (self.position[0] + self._bg_image.get_rect().centerx - self._title_label.size[0] / 2 + 10,
             self.position[1] + 3)
        )
        self.socket_group = RadioGroup()
        self.socket1 = BeeSocket(parent=self, socket_type=BeeSocketType.ALL,
                                 group=self.socket_group, position=(self.position[0] + 102, self.position[1] + 135))
        self.socket1.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
        self.dna_image = pygame.image.load("{0}/dna1.png".format(self._res_dir)).convert_alpha()
        self.dna_rect = self.dna_image.get_rect()
        self.dna_rect.x = self.socket1.position[0] + self.socket1.size[1] + 12
        self.dna_rect.y = self.socket1.get_rect().centery - self.dna_rect.height / 2
        self.socket2 = BeeSocket(parent=self, socket_type=BeeSocketType.ALL,
                                 group=self.socket_group,
                                 position=(self.dna_rect.x + self.dna_rect.width + 7, self.socket1.position[1]))
        self.socket2.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")

        upgrade_label = TextLabel(parent=self, text=self.parent.localization.get_string("upgrade_button"), font_size=18)
        self.upgrade_button = TextButton(parent=self,
                                         normal_image_path="start_quest_btn_normal.png",
                                         text_label=upgrade_label, text_padding=(40, 4))
        self.upgrade_button.set_image_by_state(ButtonState.HOVERED, "start_quest_btn_hover.png")
        self.upgrade_button.set_image_by_state(ButtonState.LOCKED, "start_quest_btn_locked.png")
        self.upgrade_button.lock()
        self.upgrade_button.set_position((self.socket1.position[0],
                                          self.socket2.position[1] + self.socket2.size[1] + 15))
        self.upgrade_button.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.upgrade()})

        self.result_socket = BeeSocket(parent=self,
                                       group=self.socket_group, position=(0, 0), socket_type=BeeSocketType.ALL)
        self.result_socket.set_image_by_state(ButtonState.SELECTED, "socket5_normal.png")
        self.result_socket.set_image_by_state(ButtonState.LOCKED, "socket3_normal.png")
        self.result_socket.lock()
        self.result_socket.set_position(
            (self.upgrade_button.get_rect().centerx - self.result_socket.size[1] / 2,
             self.upgrade_button.position[1] + self.upgrade_button.size[1] + 15)
        )
        self.result_socket.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.pick_new_bee()})

        self.info_block_image = pygame.image.load("{0}/modify_popup1_info.png".format(self._res_dir))
        self.info_block_rect = self.info_block_image.get_rect()
        self.info_text_label = TextLabel(parent=self, text=self.parent.localization.get_string("upgrade_button"),
                                         font_size=14)

        self.info_block_rect.x = self.upgrade_button.position[0] + self.upgrade_button.size[0] + 95
        self.info_block_rect.y = self.position[1] + 71
        self.info_text_label.set_position(
            (self.info_block_rect.centerx - self.info_text_label.size[0] / 2, self.info_block_rect.y)
        )

        name_label = MultilineTextLabel(parent=self, font_size=14, line_length=220,
                                        position=(self.info_block_rect.x + 25, self.info_block_rect.y + 40))

        generation_label = TextLabel(parent=self, font_size=14,
                                     position=(name_label.position[0], name_label.position[1] + name_label.size[1]))

        level_label = TextLabel(parent=self, font_size=14,
                                position=(generation_label.position[0],
                                          generation_label.position[1] + generation_label.size[1]))

        xp_label = TextLabel(parent=self, font_size=14,
                             position=(
                                 level_label.position[0],
                                 level_label.position[1] + level_label.size[1]))

        speed_label = TextLabel(parent=self, font_size=14,
                                position=(
                                    xp_label.position[0],
                                    xp_label.position[1] + xp_label.size[1]))

        hp_label = TextLabel(parent=self, font_size=14,
                             position=(
                                 speed_label.position[0],
                                 speed_label.position[1] + speed_label.size[1]))

        bonus_list_label = MultilineTextLabel(parent=self, font_size=14, line_length=220,
                                              position=(
                                                  hp_label.position[0],
                                                  hp_label.position[1] + hp_label.size[1]))

        self.info_group = RenderGroup(parent=self,
                                      data={"b_name": name_label, "b_gen": generation_label, "b_level": level_label,
                                            "b_exp": xp_label, "b_speed": speed_label, "b_hp": hp_label,
                                            "b_bonus": bonus_list_label})

        self.bee_list_view = ListView(parent=self, size=(625, 253), padding=(30, 9), item_distance=(15, 15),
                                      position=(
                                          self.position[0] + 9,
                                          self.info_block_rect.y + self.info_block_rect.height - 6)
                                      )
        self.bee_list_view.set_image("{0}/modify_popup1_bee_list.png".format(self._res_dir))

        db = Database.get_instance()
        worker_dna_name = db.get_resource_by_id(3).locale_name
        warrior_dna_name = db.get_resource_by_id(4).locale_name
        queen_dna_name = db.get_resource_by_id(5).locale_name

        dna_list = []
        for r in self.parent.player.resources.bag:
            if r.locale_name == worker_dna_name:
                for i in range(r.value):
                    dna_list.append(DNAEntity(parent=self, dna_type="worker", r=r))
            if r.locale_name == warrior_dna_name:
                for i in range(r.value):
                    dna_list.append(DNAEntity(parent=self, dna_type="warrior", r=r))
            if r.locale_name == queen_dna_name:
                for i in range(r.value):
                    dna_list.append(DNAEntity(parent=self, dna_type="queen", r=r))

        for b in itertools.chain(dna_list,
                                 self.parent.player.farm.out_of_hive_bee_list,
                                 self.parent.player.farm.bees_from_all_hives):
            self.add_bee_to_list(b)

        self.socket1.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket()})
        self.socket1.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_bee_from_socket(self.socket1)})
        self.socket1.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.reload_bee_info(self.socket1.bee)})

        self.socket2.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket()})
        self.socket2.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_bee_from_socket(self.socket2)})
        self.socket2.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.reload_bee_info(self.socket2.bee)})

        self.clear_bee_info()

        self.parent.nest_group.stop_handle()

    def destroy(self):
        if not self.result_socket.is_locked:
            self.pick_new_bee()
        self.parent.nest_group.start_handle()
        super().destroy()

    def kill_bee(self, socket: BeeSocket) -> None:
        self.parent.player.farm.kill_bee(socket.bee)
        for h in self.parent.nest_group.buttons:
            for bs in h.nest_group.buttons:
                if bs.bee:
                    if bs.bee == socket.bee:
                        del bs.bee
                        break
        del socket.bee

    def pick_new_bee(self):
        self.parent.player.farm.add_out_of_hive_bee(self.result_socket.bee)
        self.add_bee_to_list(self.result_socket.bee)
        del self.result_socket.bee
        self.result_socket.lock()

    @staticmethod
    def parse_code(code) -> str:
        return ''.join(sorted(code, reverse=any(char.isdigit() for char in code)))

    def upgrade(self):
        self.upgrade_button.lock()

        valid_codes = ["AA", "BB", "AB", "A1", "B2", "11", "22", "33"]

        dna_code = ModifyMenu.parse_code(self.socket1.bee.dna_code + self.socket2.bee.dna_code)
        if dna_code not in valid_codes:
            return

        if dna_code == "33":
            bee = BeeQueen(parent=self.parent.player)
        else:
            warrior_mod = 2

            if "B" in dna_code:
                warrior_mod += 4

            warrior_percent = (self.socket1.bee.current_level + self.socket2.bee.current_level) * warrior_mod

            if dna_code == "BB":
                warrior_percent = 75

            chance = random.random() * 100

            if chance <= warrior_percent or dna_code == "22":
                bee = BeeWarrior(parent=self.parent.player)
            else:
                bee = BeeWorker(parent=self.parent.player)

            chance = random.random() * 100
            if dna_code in ["AA", "BB", "AB"]:
                if chance <= 45:
                    t1 = self.socket1.bee.bonus
                    t2 = self.socket2.bee.bonus
                    bonus_chance = 75 if self.socket1.bee.generation > self.socket2.bee.generation else 25
                    if bonus_chance < random.random() * 100:
                        bee.bonus = t1
                    else:
                        bee.bonus = t2
                    bee.modify_bonus()
                    bee.hp_mod = max(self.socket1.bee.hp_mod, self.socket2.bee.hp_mod)
                    bee.speed_mod = max(self.socket1.bee.speed_mod, self.socket2.bee.speed_mod)
                    mod = "bonus"
                else:
                    random_param = random.randint(1, 2)
                    if random_param == 1:
                        up = (self.socket1.bee.speed + self.socket2.bee.speed) \
                             * ((self.socket1.bee.current_level + self.socket2.bee.current_level) / 2) / 100
                        bee.speed_mod = up
                        bee.hp_mod = max(self.socket1.bee.hp_mod, self.socket2.bee.hp_mod)
                        mod = "speed"
                    else:
                        bee.hp_mod = math.ceil((((self.socket1.bee.current_hp * 10) / 100)
                                                + ((self.socket2.bee.current_hp * 10) / 100)) / 2)
                        bee.current_hp = bee.max_hp
                        bee.speed_mod = max(self.socket1.bee.speed_mod, self.socket2.bee.speed_mod)
                        mod = "health"

                bee.upgrade_name(mod)
                bee.generation = max(self.socket1.bee.generation, self.socket2.bee.generation) + 1

        self.kill_bee(self.socket1)
        self.kill_bee(self.socket2)
        self.result_socket.unlock()
        self.result_socket.select()
        self.result_socket.bee = bee
        self.reload_bee_info()

    def add_bee_to_list(self, b: Bee) -> None:
        i = ListItem(parent=self, data=b, normal_image_path="holder1.png", center=True)
        i.set_image_by_state(ButtonState.LOCKED, "holder1_lock.png")
        i.set_image_by_state(ButtonState.HOVERED, "holder1_hover.png")
        i.add_action({ButtonEventType.ON_CLICK_LB: lambda e=i: self.select_bee(e)})
        i.add_action({ButtonEventType.ON_HOVER_ON: lambda e=i.data: self.reload_bee_info(e)})
        i.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.reload_bee_info()})
        self.bee_list_view.add_item(i)

    def remove_bee_from_socket(self, socket: BeeSocket) -> None:
        socket.select()
        if self.socket_group.current_button.bee:
            self.add_bee_to_list(self.socket_group.current_button.bee)
            del self.socket_group.current_button.bee
            self.clear_bee_info()
            self.upgrade_button.lock()

    def select_bee(self, list_item: ListItem) -> None:
        if self.socket_group.current_button:
            if self.socket_group.current_button.bee:
                self.remove_bee_from_socket(self.socket_group.current_button)

            self.socket_group.current_button.bee = list_item.data
            self.bee_list_view.remove_item(list_item)

        if self.socket1.bee and self.socket2.bee:
            self.upgrade_button.unlock()
        else:
            self.upgrade_button.lock()

        self.reload_bee_info()

    def add_bee_to_socket(self) -> None:
        if self.socket_group.current_button:
            if self.socket_group.current_button.bee:
                self.reload_bee_info()
            else:
                self.clear_bee_info()

    def clear_bee_info(self) -> None:
        for k, v in self.info_group.group.items():
            v.set_text(text=self.parent.localization.get_string(k))
        self.set_info_position()

    def set_info_position(self):
        self.info_group["b_name"].set_position((self.info_block_rect.x + 25, self.info_block_rect.y + 40))

        self.info_group["b_gen"].set_position((self.info_group["b_name"].position[0],
                                               self.info_group["b_name"].position[1]
                                               + self.info_group["b_name"].size[1]))

        self.info_group["b_level"].set_position((self.info_group["b_gen"].position[0],
                                                 self.info_group["b_gen"].position[1]
                                                 + self.info_group["b_gen"].size[1]))
        self.info_group["b_exp"].set_position((self.info_group["b_level"].position[0],
                                               self.info_group["b_level"].position[1]
                                               + self.info_group["b_level"].size[1]))
        self.info_group["b_speed"].set_position((self.info_group["b_exp"].position[0],
                                                 self.info_group["b_exp"].position[1]
                                                 + self.info_group["b_exp"].size[1]))
        self.info_group["b_hp"].set_position((self.info_group["b_speed"].position[0],
                                              self.info_group["b_speed"].position[1]
                                              + self.info_group["b_speed"].size[1]))
        self.info_group["b_bonus"].set_position((self.info_group["b_hp"].position[0],
                                                 self.info_group["b_hp"].position[1]
                                                 + self.info_group["b_hp"].size[1]))

    def reload_bee_info(self, b: Bee = None) -> None:
        if b is None and self.socket_group.current_button:
            b = self.socket_group.current_button.bee
        if not b:
            return

        if isinstance(b, DNAEntity):
            self.info_group.hide()
            self.info_group["b_name"].set_text(
                text="{0} {1}".format(self.parent.localization.get_string("b_desc"), b.resource.locale_desc)
            )

            self.info_group["b_name"].show()
        else:
            self.info_group.show()

        try:
            self.info_group["b_name"].set_text(
                text="{0} {1}".format(self.parent.localization.get_string("b_name"), b.name))

            self.info_group["b_gen"].set_text(
                text="{0} {1}".format(self.parent.localization.get_string("b_gen"), b.generation))

            self.info_group["b_level"].set_text(
                text="{0} {1}".format(self.parent.localization.get_string("b_level"), b.current_level)
            )

            self.info_group["b_exp"].set_text(
                text="{0} {1}/{2}".format(self.parent.localization.get_string("b_exp"), b.current_xp, b.max_xp)
            )

            if isinstance(b, BeeQueen):
                self.info_group["b_speed"].hide()
                self.info_group["b_hp"].hide()
                self.info_group["b_bonus"].hide()
            else:
                self.info_group["b_speed"].show()
                self.info_group["b_hp"].show()
                self.info_group["b_bonus"].show()

                self.info_group["b_speed"].set_text(
                    text="{0} {1}".format(self.parent.localization.get_string("b_speed"), b.speed))

                self.info_group["b_hp"].set_text(
                    text="{0} {1}/{2}".format(self.parent.localization.get_string("b_hp"), b.current_hp, b.max_hp)
                )
                self.info_group["b_bonus"].set_text(
                    text="{0} {1}".format(self.parent.localization.get_string("b_bonus"), b.bonus.description)
                )
        except AttributeError:
            pass
        except KeyError as ky:
            field = str(ky).replace('\'', '')
            print(field)
            self.info_group[field].hide()

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.socket_group.draw(screen)
        self.upgrade_button.draw(screen)
        screen.blit(self.dna_image, self.dna_rect)
        screen.blit(self.info_block_image, self.info_block_rect)
        self.info_text_label.draw(screen)
        self.bee_list_view.draw(screen)
        self.info_group.draw(screen)

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)
        self.socket_group.handle_event(event)
        self.upgrade_button.handle_event(event)
        self.bee_list_view.handle_event(event)
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         self.bee_list_view.item_padding = (30, 8)
