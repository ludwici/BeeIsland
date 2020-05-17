import pygame
from pygame.event import Event

from src import Constants
from src.BeeFamily.Bee import Bee
from src.BeeSocket import BeeSocket
from src.Scenes.Scene import Scene
from src.UI.Button import Button, ButtonEventType, ButtonState
from src.UI.ListItem import ListItem
from src.UI.ListView import ListView
from src.UI.MultilineTextLabel import MultilineTextLabel
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioGroup import RadioGroup
from src.UI.TextButton import TextButton
from src.UI.TextLabel import TextLabel


class ModifyPopup(PopupNotify):
    count = 0

    def __init__(self, parent: Scene) -> None:
        PopupNotify.__init__(self, parent=parent)
        self.close_btn = Button(parent=self, normal_image_path="../res/images/buttons/close_button1.png")
        self.close_btn.set_image_by_state(ButtonState.HOVERED, "../res/images/buttons/close_button1_hover.png")
        self.close_btn.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.destroy()})

        self._time_to_kill = 0
        self.set_background("../res/images/modify_popup1.png")
        position = (Constants.WINDOW_W / 2 - self.bg_rect.width / 2, 70)
        self.set_position(position)
        self.close_btn.set_position(position=(self._rect.topright[0] - 50, self._rect.topright[1] - 10))

        self.title_label = TextLabel(parent=self, text="Улучшение", position=self.position, font_name="segoeprint",
                                     font_size=16, bold=True, color=(159, 80, 17))
        self.title_label.set_position(
            (self.position[0] + self.bg_rect.centerx - self.title_label.get_size()[0] / 2 + 10, self.position[1] + 3)
        )
        self.socket_group = RadioGroup()
        self.socket1 = BeeSocket(parent=self, normal_image_path="../res/images/buttons/socket1_normal.png",
                                 group=self.socket_group, position=(self.position[0] + 102, self.position[1] + 135))
        self.socket1.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")
        self.dna_image = pygame.image.load("../res/images/dna1.png").convert_alpha()
        self.dna_rect = self.dna_image.get_rect()
        self.dna_rect.x = self.socket1.position[0] + self.socket1.get_size()[1] + 12
        self.dna_rect.y = self.socket1.get_rect().centery - self.dna_rect.height / 2
        self.socket2 = BeeSocket(parent=self, normal_image_path="../res/images/buttons/socket1_normal.png",
                                 group=self.socket_group,
                                 position=(self.dna_rect.x + self.dna_rect.width + 7, self.socket1.position[1]))
        self.socket2.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")

        upgrade_label = TextLabel(parent=self, text="Улучшить", position=(0, 0), font_name="segoeprint", font_size=18,
                                  color=(159, 80, 17))
        self.upgrade_button = TextButton(parent=self, normal_image_path="../res/images/buttons/start_quest_btn.png",
                                         text_label=upgrade_label, text_padding=(40, 4))
        self.upgrade_button.set_position((self.socket1.position[0],
                                          self.socket2.position[1] + self.socket2.get_size()[1] + 15))

        self.result_socket = BeeSocket(parent=self, normal_image_path="../res/images/buttons/socket1_normal.png",
                                       group=self.socket_group, position=(0, 0))
        self.result_socket.set_image_by_state(ButtonState.SELECTED, "../res/images/buttons/socket5_normal.png")
        self.result_socket.set_image_by_state(ButtonState.LOCKED, "../res/images/buttons/socket3_normal.png")
        self.result_socket.lock()
        self.result_socket.set_position(
            (self.upgrade_button.get_rect().centerx - self.result_socket.get_size()[1] / 2,
             self.upgrade_button.position[1] + self.upgrade_button.get_size()[1] + 15)
        )

        self.info_block_image = pygame.image.load("../res/images/modify_popup1_info.png")
        self.info_block_rect = self.info_block_image.get_rect()
        self.info_text_label = TextLabel(parent=self, text="Информация", position=(0, 0), font_name="segoeprint",
                                         font_size=14, color=(159, 80, 17))

        self.info_block_rect.x = self.upgrade_button.position[0] + self.upgrade_button.get_size()[0] + 95
        self.info_block_rect.y = self.position[1] + 71
        self.info_text_label.set_position(
            (self.info_block_rect.centerx - self.info_text_label.get_size()[0] / 2, self.info_block_rect.y)
        )

        self.name_label = TextLabel(parent=self, text="",
                                    position=(self.info_block_rect.x + 25, self.info_block_rect.y + 40),
                                    font_name="segoeprint", font_size=14, color=(159, 80, 17))
        print(self.name_label.position)

        self.level_label = TextLabel(parent=self, text="",
                                     position=(self.name_label.position[0],
                                               self.name_label.position[1] + self.name_label.get_size()[1]),
                                     font_name="segoeprint", font_size=14, color=(159, 80, 17))

        self.xp_label = TextLabel(parent=self, text="",
                                  position=(
                                      self.level_label.position[0],
                                      self.level_label.position[1] + self.level_label.get_size()[1]),
                                  font_name="segoeprint", font_size=14, color=(159, 80, 17))

        self.speed_label = TextLabel(parent=self, text="",
                                     position=(
                                         self.xp_label.position[0],
                                         self.xp_label.position[1] + self.xp_label.get_size()[1]),
                                     font_name="segoeprint",
                                     font_size=14, color=(159, 80, 17))

        self.hp_label = TextLabel(parent=self, text="",
                                  position=(
                                      self.speed_label.position[0],
                                      self.speed_label.position[1] + self.speed_label.get_size()[1]),
                                  font_name="segoeprint", font_size=14, color=(159, 80, 17))

        self.bonus_list_label = MultilineTextLabel(parent=self, text="",
                                                   position=(
                                                       self.hp_label.position[0],
                                                       self.hp_label.position[1] + self.hp_label.get_size()[1]),
                                                   font_name="segoeprint",
                                                   font_size=14, color=(159, 80, 17), line_length=230)

        self.bee_list_view = ListView(parent=self,
                                      position=(
                                          self.position[0] + 9,
                                          self.info_block_rect.y + self.info_block_rect.height - 6),
                                      padding=(45, 24))
        self.bee_list_view.set_image("../res/images/modify_popup1_bee_list.png")

        for b in self.parent.player.farm.out_of_hive_bee_list:
            self.add_bee_to_list(b)

        self.socket1.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket()})
        self.socket1.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_bee_from_socket()})
        self.socket2.add_action({ButtonEventType.ON_CLICK_LB: lambda: self.add_bee_to_socket()})
        self.socket2.add_action({ButtonEventType.ON_CLICK_RB: lambda: self.remove_bee_from_socket()})

        self.clear_bee_info()

    def add_bee_to_list(self, b: Bee) -> None:
        i = ListItem(parent=self, data=b, normal_image_path="../res/images/holder1.png")
        i.set_image_by_state(ButtonState.LOCKED, "../res/images/holder1_lock.png")
        i.set_image_by_state(ButtonState.HOVERED, "../res/images/holder1_hover.png")
        i.add_action({ButtonEventType.ON_CLICK_LB: lambda e=i: self.select_bee(e)})
        i.add_action({ButtonEventType.ON_HOVER_ON: lambda e=i.data: self.reload_bee_info(e)})
        i.add_action({ButtonEventType.ON_HOVER_OUT: lambda: self.clear_bee_info()})
        self.bee_list_view.add_item(i)

    def remove_bee_from_socket(self) -> None:
        if self.socket_group.current_button is not None:
            if self.socket_group.current_button.bee is not None:
                self.add_bee_to_list(self.socket_group.current_button.bee)
                del self.socket_group.current_button.bee
                self.clear_bee_info()

    def select_bee(self, list_item: ListItem) -> None:
        if self.socket_group.current_button is not None:
            self.socket_group.current_button.bee = list_item.data
            self.bee_list_view.remove_item(list_item)

    def add_bee_to_socket(self) -> None:
        print(self.socket_group.current_button.bee)
        if self.socket_group.current_button is not None:
            if self.socket_group.current_button.bee is not None:
                self.reload_bee_info()
            else:
                self.clear_bee_info()

    def clear_bee_info(self) -> None:
        self.name_label.set_text("Имя:")
        self.level_label.set_text("Уровень:")
        self.xp_label.set_text("Опыт:")
        self.speed_label.set_text("Скорость:")
        self.hp_label.set_text("Здоровье:")
        self.bonus_list_label.set_text("Бонусы:")

    def reload_bee_info(self, b: Bee = None) -> None:
        if b is None and self.socket_group.current_button is not None:
            b = self.socket_group.current_button.bee
        self.name_label.set_text("Имя: {}".format(b.name))
        self.level_label.set_text("Уровень: {}".format(b.current_level))
        self.xp_label.set_text("Опыт: {0}/{1}".format(b.current_xp, b.max_xp))
        self.speed_label.set_text("Скорость: {}".format(b.speed))
        self.hp_label.set_text("Здоровье: {0}/{1}".format(b.current_hp, b.max_hp))
        self.bonus_list_label.set_text("Бонусы: +10% очков")

    @classmethod
    def create(cls, scene: Scene, *args, **kwargs) -> "ModifyPopup":
        if ModifyPopup.count == 0:
            m = cls(parent=scene)
            m.show()
        else:
            m = scene.find_drawable_by_type(ModifyPopup)

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
        self.bee_list_view.draw(screen)
        self.name_label.draw(screen)
        self.level_label.draw(screen)
        self.xp_label.draw(screen)
        self.speed_label.draw(screen)
        self.hp_label.draw(screen)
        self.bonus_list_label.draw(screen)

    def handle_event(self, event: Event) -> None:
        self.close_btn.handle_event(event)
        self.socket_group.handle_event(event)
        self.upgrade_button.handle_event(event)
        self.bee_list_view.handle_event(event)
