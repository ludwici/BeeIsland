import pygame

from src.Player import Player
from src.Windows.MapWindow import MapWindow


def main():
    main_window = MapWindow()
    while main_window.loop():
        pass

    # p = Player()


if __name__ == "__main__":
    main()
