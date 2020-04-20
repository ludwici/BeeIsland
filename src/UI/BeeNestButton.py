import pygame

from src.BeeNest import BeeNest
from src.BeeSocket import BeeSocket
from src.UI.Button import Button
from src.UI.PopupNotify import PopupNotify
from src.UI.RadioGroup import RadioGroup


class BeeNestButton(Button):
    def __init__(self, parent, path_to_image: str, hovered_image: str = "", position: (int, int) = (0, 0)) -> None:
        Button.__init__(self, parent=parent, path_to_image=path_to_image, hovered_image=hovered_image,
                        position=position)
        self.hive = None
        self.add_action(self.buy_hive)
        self.nest_group = RadioGroup()

    def __init_hives(self) -> None:
        positions = list()
        positions.append((-33, -41))
        positions.append((positions[0][0] + 36 + 48, positions[0][1]))
        positions.append((-9 - 48, positions[0][1] + 18 + 42))
        positions.append((positions[2][1] + 48 + 9, positions[0][1] + 18 + 42))
        positions.append((-31, 40 + 42))
        positions.append((positions[0][0] + 36 + 48, 40 + 42))
        for i in range(6):
            lock = i >= self.hive.max_size
            BeeSocket(parent=self, path_to_image="../res/images/buttons/socket1_normal.png",
                      selected_image="../res/images/buttons/socket5_normal.png", group=self.nest_group, is_locked=lock,
                      position=((self.position[0] + positions[i][0]), self.position[1] + positions[i][1]))
        BeeSocket(parent=self, path_to_image="../res/images/buttons/socket4_normal.png",
                  selected_image="../res/images/buttons/socket5_normal.png", group=self.nest_group,
                  position=((self.position[0] + positions[2][0] + 18 + 48), self.position[1] + positions[2][1]))

    def show_honeycombs(self) -> None:
        print("{0}/{1} пчёл".format(self.hive.size, self.hive.max_size))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.hive:
            self.nest_group.draw(screen)

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if self.hive:
            self.nest_group.handle_event(event)

    def buy_hive(self) -> None:
        if self.parent.player.can_buy_new_hive:
            self.hive = BeeNest()
            self.parent.player.farm.add_hive(self.hive)
            self.set_image(path="../res/images/bee/hive/hive1_normal.png")
            self.hovered_image = self.normal_image
            self.__init_hives()
            self.action_list.clear()
            self.add_action(self.show_honeycombs)
        else:
            PopupNotify.create(scene=self.parent, text="Вы пока не можете купить это гнездо")
