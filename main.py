import os
import platform
import sys

from src import Constants
from src.RenderWindow import RenderWindow


def main():
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    # try:
    print(platform.architecture()[0], sys.maxsize > 2 ** 32)
    main_window = RenderWindow(width=Constants.WINDOW_W, height=Constants.WINDOW_H)
    main_window.start()
    # except Exception as ex:
    #     print(ex)


if __name__ == "__main__":
    main()
