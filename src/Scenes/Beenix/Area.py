import random
from typing import Tuple

import pygame


class InverseArea(pygame.sprite.Sprite):
    def __init__(self, area, mask):
        super(InverseArea, self).__init__()
        self.width, self.height = area.size
        self.image = area.image
        self.image.set_colorkey((255, 255, 255))
        self.mask = mask
        self.rect = self.image.get_rect()

    def update_mask(self, mask):
        self.mask = mask


class Area(pygame.sprite.Sprite):

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.size = (800, 600)
        self.image = pygame.Surface(self.size)  # lgtm [py/call/wrong-arguments]
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.position = self.rect.x, self.rect.y

        self.mask = pygame.mask.from_surface(self.image)
        self.color = (182, 81, 14)
        self.border_size = 20
        border_color = self.color
        pygame.draw.rect(self.image, border_color, (0, 0, self.size[0], self.border_size))
        pygame.draw.rect(self.image, border_color, (0, 0, self.border_size, self.size[1]))
        pygame.draw.rect(self.image, border_color, (0, self.size[1] - self.border_size, self.size[0], self.border_size))
        pygame.draw.rect(self.image, border_color, (self.size[0] - self.border_size, 0, self.border_size, self.size[1]))
        self.area_inverse = InverseArea(self, pygame.mask.from_surface(self.image).invert())
        self.update_mask()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update_mask(self) -> None:
        self.mask = pygame.mask.from_surface(self.image)
        mask_inverse = pygame.mask.from_surface(self.image)
        mask_inverse.invert()
        self.area_inverse.update_mask(mask_inverse)

    @staticmethod
    def middle_of(p1, p2) -> Tuple[float, float]:
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

    def check_open_sides(self, points, line_width, vertical, spiders) -> Tuple[float, float]:
        point = Area.middle_of(points[0], points[1])
        sides = [(line_width, 0), (-line_width, 0), (0, -line_width), (0, line_width)]
        fill_points = [side for side in sides if not self.contains((point[0] + side[0], point[1] + side[1]))]
        better_side = Area.find_better_side(points, vertical, spiders)
        if better_side:
            fill_points1 = [p for p in fill_points if p[0] > 0 or p[1] > 0]
        else:
            fill_points1 = [p for p in fill_points if p[0] < 0 or p[1] < 0]
        if len(fill_points1) > 0:
            fill_point = fill_points1[0]
        else:
            return self.check_open_sides(points[1: -1], line_width, vertical, spiders)
        return point[0] + fill_point[0], point[1] + fill_point[1]

    def fill(self, x, y, color) -> None:
        x = int(x)
        y = int(y)
        self.pixels = pygame.PixelArray(self.image)  # lgtm [py/call/wrong-arguments]
        old_color = self.pixels[x, y]

        if old_color == color:
            return

        stack = [(x, y)]
        w, h = self.rect.w, self.rect.h
        while stack:
            cur_point = stack.pop()
            x1, y1 = cur_point

            while x1 >= self.rect.x and self.pixels[x1, y1] == old_color:
                x1 -= 1
            x1 += 1

            above = False
            below = False

            while x1 < w and self.pixels[x1, y1] == old_color:
                self.pixels[x1, y1] = color

                if not above and y1 > self.rect.y and self.pixels[x1, y1 - 1] == old_color:
                    stack.append((x1, y1 - 1))
                    above = True
                elif above and y1 < h - 1 and self.pixels[x1, y1 - 1] != old_color:
                    above = False

                if not below and y1 < h - 1 and self.pixels[x1, y1 + 1] == old_color:
                    stack.append((x1, y1 + 1))
                    below = True
                elif below and y1 < h - 1 and self.pixels[x1, y1 + 1] != old_color:
                    below = False

                x1 += 1
        self.pixels = None
        self.update_mask()

    def add(self, points) -> None:
        pygame.draw.polygon(self.image, self.color, points)
        self.update_mask()

    def contains(self, r: (int, int)) -> bool:
        pos = int(r[0]), int(r[1])
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        return self.rect.collidepoint(*pos) and self.mask.get_at(pos_in_mask)

    @staticmethod
    def find_better_side(points, vertical, spiders) -> bool:
        positive = negative = 0
        for s in spiders:
            if not s.alive:
                continue
            s_x, s_y = s.rect.center
            limit = Area.find_line(points, (s_x, s_y), vertical)
            if vertical:
                if s_x > limit:
                    positive += 1
                else:
                    negative += 1
            else:
                if s_y > limit:
                    positive += 1
                else:
                    negative += 1
        return positive < negative

    @staticmethod
    def find_line(points, point, vertical) -> int:
        for i in range(len(points) - 1):
            cond = int(vertical)
            if min(points[i][cond], points[i + 1][cond]) <= point[cond] <= max(points[i][cond], points[i + 1][cond]):
                return points[i][int(not vertical)]

        return random.choice(points)[int(not vertical)]
