from itertools import cycle
from random import shuffle, choice
from typing import List, Tuple, Union, Generator, Any

import pygame
from pygame.rect import Rect

from src.Animation import Animation
from src.Scenes.Match3.Flower import FlowersData, Flower
from src.Utils import get_distance


class FlowersGrid:
    __slots__ = ("tile_size", "position", "rows_count", "cols_count", "rect", "cells", "recheck", "done", "max_bonus",
                 "score_multiplier", "bonus", "score", "elapsed", "spin_speed", "level", "num_combos", "bonus_cooldown",
                 "rows", "columns", "possible_matches", "animations", "spin_animations", "flower_combos", "no_moves")

    def __init__(self, position: (int, int), size: (int, int)) -> None:
        self.tile_size = 64, 64
        self.position = position
        self.rows_count = size[0]
        self.cols_count = size[1]
        self.rect = Rect(position[0], position[1], self.cols_count * self.tile_size[0],
                         self.rows_count * self.tile_size[1])
        self.cells = None
        self.recheck = False
        self.done = False
        self.max_bonus = 1000
        self.bonus = int(self.max_bonus * .5)
        self.score_multiplier = 1
        self.score = 0
        self.elapsed = 0
        self.spin_speed = 100
        self.level = 1
        self.bonus_cooldown = .01
        self.num_combos = len(FlowersData)  # TODO: add dependence on difficulty level
        self.rows = []
        self.columns = []
        self.possible_matches = None
        self.animations = pygame.sprite.Group()
        self.spin_animations = pygame.sprite.Group()
        self.flower_combos = self.make_combos()
        self.make_cells()
        self.fill()

    def draw(self, surface: pygame.Surface) -> None:
        for cell in self.cells.values():
            if cell.flower:
                cell.flower.draw(surface)

    def update(self, dt: float) -> None:
        self.elapsed += dt
        self.animations.update(dt)
        self.spin_animations.update(dt)
        if not self.animations:
            self.update_cells()

            empty_cells = any(not cell.flower for cell in self.cells.values())
            if empty_cells:
                self.fill_flowers()

            if not self.animations and self.recheck and not empty_cells:
                matches = self.find_all_matches()
                self.clear_matches(matches)
                if not any((not cell.flower for cell in self.cells.values())):
                    self.possible_matches = self.find_moves()
                    if not self.possible_matches:
                        self.no_moves = True
                        print("NO MOVES")
                self.recheck = False

    def make_cells(self) -> None:
        self.cells = \
            {
                (x, y): GridCell(self.position, (x, y), self.tile_size)
                for x in range(self.cols_count)
                for y in range(self.rows_count)
            }
        for c in self.cells:
            self.cells[c].get_neighbor_cells(self.cells)

        for y in range(self.rows_count):
            row = []
            for x in range(self.cols_count):
                row.append(self.cells[(x, y)])
            self.rows.append(row)

        for x in range(self.cols_count):
            col = []
            for y in range(self.rows_count):
                col.append(self.cells[(x, y)])
            self.columns.append(col)

    def make_combos(self) -> List[FlowersData]:
        colors = [FlowersData.YELLOW, FlowersData.PURPLE, FlowersData.BLUE, FlowersData.GREEN, FlowersData.TURQUOISE]
        shuffle(colors)
        colors = cycle(colors)

        combos = []
        for _ in range(self.num_combos):
            combos.append((next(colors)))
        return combos

    def fill(self) -> None:
        for c in self.cells.values():
            color = choice(self.flower_combos)
            c.flower = Flower((c.rect.x, c.rect.y), color)

        while True:
            matches = self.find_all_matches()
            if not matches:
                break
            for m in matches:
                for i in m:
                    color = choice(self.flower_combos)
                    c = self.cells[i]
                    c.flower = Flower((c.rect.x, c.rect.y), color)

    def find_all_matches(self) -> List[List[Tuple[int, int]]]:
        matches = self.find_matches(is_col=False)
        matches.extend(self.find_matches(is_col=True))
        return matches

    def find_matches(self, is_col) -> List[List[Tuple[int, int]]]:
        matches = []
        source = self.columns if is_col else self.rows
        for i, data in enumerate(source):
            colors = (cell.flower.color if cell.flower else None for cell in data)
            data_matches = FlowersGrid.find_repeats(colors, 3)
            for match in data_matches:
                if is_col:
                    matches.append([(i, index) for index in match])
                else:
                    matches.append([(index, i) for index in match])
        return matches

    @staticmethod
    def find_repeats(iterable, min_length, excludes=None) -> \
            List[Union[Generator[int, Any, None], Generator[Union[int, Any], Any, None]]]:
        excludes = [None] if not excludes else excludes
        matches = []
        potential = None
        for i, x in enumerate(iterable):
            if not potential:
                if x not in excludes:
                    potential = [(i, x)]
            else:
                if potential[-1][1] == x:
                    potential.append((i, x))
                else:
                    if len(potential) >= min_length:
                        matches.append((p[0] for p in potential))
                    potential = [(i, x)]
        if potential and len(potential) >= min_length:
            matches.append((p[0] for p in potential))
        return matches

    def update_cells(self) -> None:
        for y in range(self.rows_count - 1, -1, -1):
            for x in range(self.cols_count):
                cell = self.cells[(x, y)]
                if cell.flower:
                    try:
                        dest = self.cells[(cell.index[0], cell.index[1] + 1)]
                        if not dest.flower:
                            cell.send_flower(dest, self.animations)
                    except KeyError:
                        pass

    def fill_flowers(self) -> None:
        for cell in self.rows[0]:
            if not cell.flower:
                topleft = cell.rect.left, cell.rect.top - cell.rect.height
                color = choice(self.flower_combos)
                cell.flower = Flower(position=topleft, color=color)
                dist = cell.rect.top - cell.flower.rect.top
                a = Animation(top=cell.rect.top, duration=int(dist), round_values=True)
                a.start(cell.flower.rect)
                self.animations.add(a)
        self.recheck = True

    def clear_matches(self, matches) -> None:
        delay = 0
        for m in sorted(matches, key=len):
            length = len(m)
            points_per = 10 * (length - 2)
            score = length * points_per * self.score_multiplier * self.level
            self.score += score
            self.bonus += length + points_per
            self.score_multiplier += 1
            delay += 250
            print("Score: {}".format(self.score))
            # centers = [self.cells[i].rect.center for i in m]
            # cx = sum((c[0] for c in centers)) / len(centers)
            # cy = sum((c[1] for c in centers)) / len(centers)
            # self.add_points_label((cx, cy), score)
            for i in m:
                self.cells[i].flower = None
        if matches:
            self.spin_up(len(matches[-1]))

    def find_moves(self) -> Tuple[Any, Tuple[int, int]]:
        for x in range(self.cols_count):
            for y in range(self.rows_count):
                cell = self.cells[(x, y)]
                flower = cell.flower
                for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    try:
                        other = self.cells[(x + d[0], y + d[1])]
                    except KeyError:
                        continue
                    other_flower = other.flower
                    cell.flower = other_flower
                    other.flower = flower
                    match = self.find_all_matches()
                    cell.flower = flower
                    other.flower = other_flower
                    if match:
                        return cell.index, d

    def reseat_flower(self, cell) -> None:
        flower = cell.flower
        if not flower:
            return

        dist = get_distance(flower.rect.topleft, cell.rect.topleft)
        if dist > 0:
            a = Animation(top=cell.rect.top, left=cell.rect.left,
                          duration=int(dist * 3), round_values=True,
                          transition="out_bounce")
            a.start(flower.rect)
            self.animations.add(a)

    def check_move(self, grabbed_tile, dest_tile) -> bool:
        existing_matches = self.find_all_matches()
        g = grabbed_tile
        d = dest_tile
        if not g or not d:
            return False
        gf = grabbed_tile.flower
        df = dest_tile.flower
        if not gf or not df:
            return False
        g.flower = df
        d.flower = gf
        valid = self.find_all_matches()
        g.flower = gf
        d.flower = df

        for m in valid:
            if m not in existing_matches:
                return True
        return False

    def spin_up(self, num) -> None:
        self.spin_animations.empty()
        speeds = {3: 10, 4: 5, 5: 2, 6: 1, 7: 1, 8: 1}
        spin_up = Animation(spin_speed=speeds[num],
                            duration=350, round_values=True)
        spin_up.callback = self.spin_down
        spin_up.start(self)
        self.spin_animations.add(spin_up)

    def spin_down(self) -> None:
        spin = Animation(spin_speed=100, duration=3500,
                         round_values=True)
        spin.start(self)
        self.spin_animations.add(spin)

    # def add_points_label(self, center_point, score):
    #     cx, cy = center_point
    #     label =


class GridCell:
    def __init__(self, position: (int, int), index: (int, int), size: (int, int)) -> None:
        self.index = index
        w, h = size
        self.rect = Rect(position[0] + (w * index[0]), position[1] + (h * index[1]), w, h)
        self.flower = None
        self.neighbors = {}

    def get_neighbor_cells(self, grid) -> None:
        offsets = \
            {
                "left": (self.index[0] - 1, self.index[1]),
                "right": (self.index[0] + 1, self.index[1]),
                "up": (self.index[0], self.index[1] - 1),
                "down": (self.index[0], self.index[1] + 1)
            }

        for off in offsets:
            self.neighbors[off] = grid[offsets[off]] if offsets[off] in grid else None

    def send_flower(self, new_cell, animations) -> None:
        dist = new_cell.rect.top - self.rect.top
        a = Animation(top=new_cell.rect.top, left=new_cell.rect.left,
                      duration=int(dist * Animation.ANIM_SPEED), round_values=True)
        a.start(self.flower.rect)
        animations.add(a)
        new_cell.flower = self.flower
        self.flower = None
