from enum import Enum

import pygame

from src.Interfaces.RenderObject import RenderObject
from src.Utils import resource_path


class Direction(Enum):
    STILL = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

    @staticmethod
    def line_direction(p1, p2) -> "Direction":
        if p1[0] < p2[0]:
            return Direction.RIGHT
        elif p1[0] > p2[0]:
            return Direction.LEFT
        elif p1[1] > p2[1]:
            return Direction.UP
        else:
            return Direction.DOWN


class Beenix(RenderObject):
    __slots__ = ("images", "movement", "speed", "points", "area", "area_size", "mask", "in_conquered", "move_keys_wasd",
                 "image")

    def __init__(self, parent, position: (int, int), area) -> None:
        RenderObject.__init__(self, parent=parent, position=position)
        self.images = dict()
        self.images.update(
            {"right": pygame.image.load("{0}/images/bee/bee1_r.png".format(resource_path("res"))).convert_alpha()})
        self.images.update(
            {"down": pygame.image.load("{0}/images/bee/bee1_d.png".format(resource_path("res"))).convert_alpha()})
        self.image = self.images["right"]
        self.image.set_colorkey((0, 0, 0))
        self.movement = Direction.STILL
        self.speed = 2
        self._rect = self.image.get_rect()
        self.points = []
        self.area = area
        self.area_size = area.rect.x, area.rect.y
        self.mask = pygame.mask.from_surface(self.image)
        self.in_conquered = False
        self.move_keys_wasd = [pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s]

    def __move_right(self, pixels) -> None:
        if self._rect.right + pixels >= self.area.rect.right - 1:
            self._rect.right = self.area.rect.right - 1
            self.movement = Direction.STILL
        else:
            self._rect.x += pixels
            self.image = self.images["right"]

    def __move_left(self, pixels) -> None:
        if self._rect.left - pixels <= self.area.rect.left - 1:
            self._rect.left = self.area.rect.left
            self.movement = Direction.STILL
        else:
            self._rect.x -= pixels
            self.image = pygame.transform.flip(self.images["right"], True, False)

    def __move_up(self, pixels) -> None:
        if self._rect.top - pixels <= self.area.rect.top - 1:
            self._rect.top = self.area.rect.top
            self.movement = Direction.STILL
        else:
            self._rect.y -= pixels
            self.image = pygame.transform.flip(self.images["down"], False, True)

    def __move_down(self, pixels) -> None:
        if self._rect.bottom + pixels >= self.area.rect.bottom - 1:
            self._rect.bottom = self.area.rect.bottom - 1
        else:
            self._rect.y += pixels
            self.image = self.images["down"]

    def change_movement(self, direction: Direction) -> None:
        self.movement = direction

    def get_pos(self) -> list:
        return list(self._rect.center)

    def __add_point(self) -> None:
        self.points.append(self.get_pos())

    def draw(self, surface: pygame.Surface) -> None:
        if len(self.points) > 1:
            self.points[-1] = list(self._rect.center)
            for i in range(len(self.points) - 1):
                pygame.draw.line(surface, (182, 81, 14), self.points[i], self.points[i + 1], 3)
        surface.blit(self.image, self._rect)

    def update(self, spiders) -> None:
        if len(self.points) > 1:
            if not self.area.contains(self.points[0]):
                direction = Direction.line_direction(self.points[0], self.points[1])
                if direction == Direction.RIGHT:
                    self.points[0][0] -= 5
                if direction == Direction.LEFT:
                    self.points[0][0] += 5
                if direction == Direction.DOWN:
                    self.points[0][1] -= 5
                if direction == Direction.UP:
                    self.points[0][1] += 5

        if self.area.contains(self.get_pos()):
            if not self.in_conquered:
                self.movement = Direction.STILL
                self.in_conquered = True
                if len(self.points) >= 2:
                    start_dir = Direction.line_direction(self.points[0], self.points[1]).value
                    end_dir = Direction.line_direction(self.points[-2], self.points[-1]).value
                    pygame.draw.lines(self.area.image, self.area.color, False, self.points, 1)
                    self.area.update_mask()

                    if start_dir == end_dir:
                        vertical = True if start_dir == 3 or start_dir == 4 else False
                        fill_point = self.area.check_open_sides(self.points, 5, vertical, spiders)
                        self.area.fill(fill_point[0], fill_point[1], self.area.color)
                    else:
                        self.__extend_point(self.points[0], start_dir, True)
                        self.__extend_point(self.points[-1], end_dir, False)
                        end = (self.points[0][0], self.points[-1][1])
                        if end not in [self.area.rect.topleft,
                                       (self.area.rect.left, self.area.rect.bottom - 1),
                                       (self.area.rect.right - 1, self.area.rect.top),
                                       (self.area.rect.right - 1, self.area.rect.bottom - 1)]:
                            end = self.points[-1][0], self.points[0][1]
                        self.points.append(end)
                        self.area.add(self.points)

                self.points = []
        elif self.in_conquered and not self.area.contains(self.get_pos()):
            self.in_conquered = False
            self.__add_point()
            self.__add_point()

        if self.movement == Direction.RIGHT:
            self.__move_right(self.speed)
        elif self.movement == Direction.LEFT:
            self.__move_left(self.speed)
        elif self.movement == Direction.UP:
            self.__move_up(self.speed)
        elif self.movement == Direction.DOWN:
            self.__move_down(self.speed)
        self.area.update_mask()

    def handle_events(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in self.move_keys_wasd:
                old_direction = self.movement.value
                new_direction = self.move_keys_wasd.index(event.key) + 1
                if not self.in_conquered:
                    if abs(old_direction - new_direction) == 1 and (
                            min(old_direction, new_direction) == 1 or min(old_direction, new_direction) == 3):
                        self.parent.wasted()
                    self.__add_point()
                self.change_movement(Direction(new_direction))

    def __extend_point(self, p, direction, start) -> None:
        if start and direction == Direction.RIGHT.value or not start and direction == Direction.LEFT.value:
            p[0] = self.area.rect.left
        elif start and direction == Direction.LEFT.value or not start and direction == Direction.RIGHT.value:
            p[0] = self.area.rect.right - 1
        elif start and direction == Direction.UP.value or (not start and direction == Direction.DOWN.value):
            p[1] = self.area.rect.bottom - 1
        else:
            p[1] = self.area.rect.top

    def is_self_destruct(self) -> bool:
        for i in range(len(self.points) - 3):
            x1, y1 = self.points[1]
            x2, y2 = self.points[i + 1]

            if min(x1, x2) <= self.points[-1][0] <= max(x1, x2) and min(y1, y2) <= self.points[-1][1] <= max(y1, y2):
                return True
        return False
