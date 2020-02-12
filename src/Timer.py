import pygame
from threading import Thread


class Timer:
    def __init__(self, mills: float) -> None:
        self.__start_time = 0
        self.__loop_thr = Thread(target=self.loop, daemon=True)
        self.in_times_actions = []
        self.after_times_actions = []
        self.time = mills
        self.current_time = 0
        self.done = False

    def loop(self) -> None:
        while not self.done:
            mills = pygame.time.get_ticks() - self.__start_time
            self.current_time = mills
            if mills >= self.time:
                self.stop()
            [m() for m in self.in_times_actions]
        [m() for m in self.after_times_actions]

    def start(self) -> None:
        self.done = False
        self.__start_time = pygame.time.get_ticks()
        self.__loop_thr.start()

    def stop(self) -> None:
        self.done = True
        self.__start_time = 0

    def __del__(self):
        print("Dtor Timer")
