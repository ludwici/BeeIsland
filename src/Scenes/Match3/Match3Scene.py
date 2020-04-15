import pygame

from pygame.event import Event

from src.Animation import Animation
from src.FlowersGrid import FlowersGrid
from src.Scenes.Scene import Scene
from src.Utils import get_distance


class Match3Scene(Scene):
    def __init__(self, main_window, player) -> None:
        Scene.__init__(self, main_window=main_window, player=player)
        self.bg_image = pygame.image.load("../res/images/quest_bg1.png").convert_alpha()
        self.grid = FlowersGrid(position=(124, 124), size=(8, 8))
        self.grabbed = None
        self.grab_point = 0, 0
        self.dest_tile = None
        self.last_click = 0
        self.click_cooldown = 250

    def on_scene_started(self) -> None:
        # TODO: Start timer and other mechanics
        print(self.scene_settings)

    def update(self, dt: float) -> None:
        self.last_click += dt
        if self.grabbed:
            current_dest = self.dest_tile
            flower = self.grabbed.flower
            if not flower:
                self.grabbed = None
                return
            gr = self.grabbed.rect
            neighbors = self.grabbed.neighbors
            x, y = pygame.mouse.get_pos()
            flower.rect.left = x - self.grab_point[0]
            flower.rect.top = y - self.grab_point[1]
            dx = abs(flower.rect.left - self.grabbed.rect.left)
            dy = abs(flower.rect.top - self.grabbed.rect.top)
            if dx >= dy:
                if flower.rect.left < gr.left:
                    if neighbors["left"]:
                        flower.rect.left = max(flower.rect.left, neighbors["left"].rect.left)
                        self.dest_tile = neighbors["left"]
                        if self.dest_tile.flower:
                            right = gr.left + (self.dest_tile.rect.right - flower.rect.left)
                            self.dest_tile.flower.rect.right = right
                    else:
                        flower.rect.left = gr.left
                elif flower.rect.right > gr.right:
                    if neighbors["right"]:
                        flower.rect.right = min(flower.rect.right, neighbors["right"].rect.right)
                        self.dest_tile = neighbors["right"]
                        if self.dest_tile.flower:
                            self.dest_tile.flower.rect.left = gr.right - (flower.rect.right - self.dest_tile.rect.left)
                    else:
                        flower.rect.right = gr.right
                flower.rect.top = gr.top
            else:
                if flower.rect.top < gr.top:
                    if neighbors["up"]:
                        flower.rect.top = max(flower.rect.top, neighbors["up"].rect.top)
                        self.dest_tile = neighbors["up"]
                        if self.dest_tile.flower:
                            self.dest_tile.flower.rect.bottom = gr.top - (flower.rect.top - self.dest_tile.rect.bottom)
                    else:
                        flower.rect.top = gr.top
                elif flower.rect.bottom > gr.bottom:
                    if neighbors["down"]:
                        flower.rect.bottom = min(flower.rect.bottom, neighbors["down"].rect.bottom)
                        self.dest_tile = neighbors["down"]
                        if self.dest_tile.flower:
                            self.dest_tile.flower.rect.top = gr.bottom - (flower.rect.bottom - self.dest_tile.rect.top)
                    else:
                        flower.rect.bottom = gr.bottom
                flower.rect.left = gr.left

            if current_dest and current_dest != self.dest_tile:
                if current_dest.flower:
                    current_dest.flower.rect.topleft = current_dest.rect.topleft

        self.grid.bonus -= self.grid.bonus_cooldown * dt
        if self.grid.bonus <= 0:  # TODO: optimize it
            self.grid.done = True

        self.grid.update(dt)
        # if self.grid.bonus >= self.grid.max_bonus:

    def handle_events(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.last_click < self.click_cooldown:
                return
            else:
                self.last_click = 0
            for cell in self.grid.cells.values():
                if cell.rect.collidepoint(event.pos) and cell.flower:
                    self.grabbed = cell
                    self.grid.score_multiplier = 1
                    self.grab_point = \
                        (
                            event.pos[0] - self.grabbed.flower.rect.left, event.pos[1] - self.grabbed.flower.rect.top
                        )
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.grabbed:
                if self.dest_tile and not self.dest_tile.flower:
                    self.grid.reseat_flower(self.grabbed)
                    return
                valid = self.grid.check_move(self.grabbed, self.dest_tile)
                if valid:
                    self.swap_tiles(self.grabbed, self.dest_tile)
                else:
                    self.grid.reseat_flower(self.grabbed)
                    self.grid.reseat_flower(self.dest_tile)
                self.grabbed = None

    def on_scene_change(self) -> None:
        super().on_scene_change()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.bg_image, self.bg_image.get_rect())
        self.grid.draw(surface)
        if self.grabbed and self.grabbed.flower:
            self.grabbed.flower.draw(surface)

    def swap_tiles(self, grabbed_tile, dest_tile) -> None:
        gf = grabbed_tile.flower
        df = dest_tile.flower
        speed = 3.5
        dist = get_distance(gf.rect.topleft, dest_tile.rect.topleft)
        if dist != 0:
            duration = int(speed * dist)
            a1 = Animation(left=dest_tile.rect.left, top=dest_tile.rect.top, duration=duration, round_values=True)
            a1.start(gf.rect)
            a2 = Animation(left=grabbed_tile.rect.left, top=grabbed_tile.rect.top, duration=duration, round_values=True)
            a2.start(df.rect)
            self.grid.animations.add(a1, a2)
        dest_tile.flower = gf
        grabbed_tile.flower = df
        self.grid.recheck = True
