import os
import sys

from src import Constants
from src.RenderWindow import RenderWindow


def main():
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    main_window = RenderWindow(width=Constants.WINDOW_W, height=Constants.WINDOW_H)
    main_window.start()


if __name__ == "__main__":
    main()
