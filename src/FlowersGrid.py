import pygame

from src.Scenes.Match3.Flower import FlowersData, Flower
from itertools import cycle
from random import shuffle, choice
from typing import List, Tuple, Union, Generator, Any
from pygame.rect import Rect


class FlowersGrid:
    def __init__(self, position: (int, int), size: (int, int)) -> None:
        self.tile_size = 64, 64
        self.position = position
        self.size = size
        self.rect = Rect(position[0], position[1], size[1] * self.tile_size[0], size[0] * self.tile_size[1])
        self.cells = None
        self.score_multiplier = 1
        self.score = 0
        self.num_combos = 4
        self.rows = []
        self.columns = []
        self.flower_combos = self.make_combos()
        self.make_cells()
        self.fill()

    def draw(self, surface: pygame.Surface) -> None:
        for cell in self.cells.values():
            if cell.flower is not None:
                cell.flower.draw(surface)

    def make_cells(self) -> None:
        self.cells = \
            {
                (x, y): GridCell(self.position, (x, y), self.tile_size)
                for x in range(self.size[1])
                for y in range(self.size[0])
            }
        for c in self.cells:
            self.cells[c].get_neighbor_cells(self.cells)

        for y in range(self.size[1]):
            row = []
            for x in range(self.size[0]):
                row.append(self.cells[(x, y)])
            self.rows.append(row)

        for x in range(self.size[0]):
            col = []
            for y in range(self.size[1]):
                col.append(self.cells[(x, y)])
            self.columns.append(col)

    def make_combos(self) -> List[FlowersData]:
        colors = [FlowersData.YELLOW, FlowersData.RED, FlowersData.BLUE, FlowersData.GREEN]
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
                    c.flower = Flower(c.rect.topleft, color)

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
                matches.append([(index, i) for index in match])
        return matches

    @staticmethod
    def find_repeats(iterable, min_length, excludes=None) -> \
            List[Union[Generator[int, Any, None], Generator[Union[int, Any], Any, None]]]:
        excludes = [None] if excludes is None else excludes
        matches = []
        potential = None
        for i, x in enumerate(iterable):
            if potential is None:
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
