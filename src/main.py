from src import Constants
from src.RenderWindow import RenderWindow


def main():
    main_window = RenderWindow(width=Constants.WINDOW_W, height=Constants.WINDOW_H)
    main_window.start()


if __name__ == "__main__":
    main()
