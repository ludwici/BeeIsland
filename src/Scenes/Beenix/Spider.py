import random

import pygame

from src.Utils import resource_path


class Spider(pygame.sprite.Sprite):

    def __init__(self, area) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._radius = 6
        self.area = area
        self.image = pygame.image.load("{0}/images/spider1.png".format(resource_path("res"))).convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.alive = True

        self._velocity_x = 0
        self._velocity_y = 0
        self.vel_x = 5
        self.vel_y = 5

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.area.border_size, self.area.rect.w - self.area.border_size - self.rect.w)
        self.rect.y = random.randint(self.area.border_size, self.area.rect.h - self.area.border_size - self.rect.h)
        self._angle = 0
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def vel_x(self) -> int:
        return self._velocity_x

    @property
    def vel_y(self) -> int:
        return self._velocity_y

    @vel_x.setter
    def vel_x(self, v) -> None:
        self.image = pygame.transform.flip(self.image, True, False)
        self._velocity_x = v

    @vel_y.setter
    def vel_y(self, v) -> None:
        self.image = pygame.transform.flip(self.image, False, True)
        self._velocity_y = v

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def collide_x(self, sprite) -> bool:
        original = self.rect.x
        collision = False
        self.rect.x += self.vel_x / 2
        if pygame.sprite.collide_mask(self, sprite):
            collision = True
        self.rect.x = original
        return collision

    def collide_y(self, sprite) -> bool:
        original = self.rect.y
        collision = False
        self.rect.y += self.vel_y / 2
        if pygame.sprite.collide_mask(self, sprite):
            collision = True
        self.rect.y = original
        return collision

    def update(self) -> None:
        size = self.area.size
        if self.area.contains(r=self.rect.center) and self.alive:
            self.alive = False

        if self.alive:
            if self.collide_x(self.area):
                self.vel_x *= -1
            if self.collide_y(self.area):
                self.vel_y *= -1
        else:
            if self.collide_x(self.area.area_inverse):
                self.vel_x *= -1
            if self.collide_y(self.area.area_inverse):
                self.vel_y *= -1

        if self.rect.left + self.vel_x / 2 < 0 or self.rect.right + self.vel_x / 2 > size[0] - 1:
            self.vel_x *= -1
        if self.rect.top + self.vel_y / 2 < 0 or self.rect.bottom + self.vel_y / 2 > size[1] - 1:
            self.vel_y *= -1
        self.rect.x += self.vel_x / 2
        self.rect.y += self.vel_y / 2

    def on_line(self, points) -> bool:
        for i in range(len(points) - 1):
            if min(points[i][0], points[i + 1][0]) <= self.rect.left <= max(points[i][0], points[i + 1][0]) or \
                    min(points[i][0], points[i + 1][0]) <= self.rect.right <= max(points[i][0], points[i + 1][0]):
                if abs(self.rect.centery - points[i][1]) < 5:
                    print(self.rect.centery - points[i][1])
                    return True
            if min(points[i][1], points[i + 1][1]) <= self.rect.top <= max(points[i][1], points[i + 1][1]) or \
                    min(points[i][1], points[i + 1][1]) <= self.rect.bottom <= max(points[i][1], points[i + 1][1]):
                if abs(self.rect.centerx - points[i][0]) < 5:
                    return True
        return False
