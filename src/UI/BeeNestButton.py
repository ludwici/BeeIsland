import pygame

from src.BeeNest import BeeNest
from src.BeeSocket import BeeSocket
from src.UI.Button import Button
from src.UI.PopupNotify import PopupNotify


class BeeNestButton(Button):
    def __init__(self, parent, path_to_image: str, hovered_image: str = "", position: (int, int) = (0, 0)):
        Button.__init__(self, parent=parent, path_to_image=path_to_image, hovered_image=hovered_image,
                        position=position)
        self.hive = None
        self.add_action(self.buy_hive)
        self.nests = []

    def __init_hives(self):
        positions = []
        positions.append((-33, -41))
        positions.append((positions[0][0] + 36 + 48, positions[0][1]))
        positions.append((-9 - 48, positions[0][1] + 18 + 42))
        positions.append((positions[2][1] + 48 + 9, positions[0][1] + 18 + 42))
        positions.append((-31, 40 + 42))
        positions.append((positions[0][0] + 36 + 48, 40 + 42))
        for i in range(6):
            if i >= self.hive.max_size:
                path = "../res/images/buttons/socket3_normal.png"
                status = False
            else:
                path = "../res/images/buttons/socket1_normal.png"
                status = True
            s = BeeSocket(parent=self, path_to_image=path, is_active=status,
                          position=((self.position[0] + positions[i][0]), self.position[1] + positions[i][1]))
            self.nests.append(s)

    def show_honeycombs(self):
        print("{0}/{1} пчёл".format(self.hive.size, self.hive.max_size))

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.hive:
            [s.draw(screen) for s in self.nests]

    def handle_event(self, event) -> None:
        super().handle_event(event)
        if self.hive:
            [s.handle_event(event) for s in self.nests]

    def buy_hive(self):
        if self.parent.player.can_buy_new_hive:
            self.hive = BeeNest()
            self.parent.player.farm.add_hive(self.hive)
            self.set_image(path="../res/images/bee/hive/hive1_normal.png")
            self.hovered_image = self.normal_image
            self.__init_hives()
            self.action_list.clear()
            self.add_action(self.show_honeycombs)
        else:
            PopupNotify.create(scene=self.parent, text="Вы не можете купить это гнездо")
