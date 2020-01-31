import pygame

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QTableWidget, QTextEdit, QWidget, QGraphicsView, QDoubleSpinBox, QPushButton

from src.Player import Player
from src.Reporter import Reporter
from src.Windows.MapWindow import MapWindow

Form, Window = uic.loadUiType("main_form.ui")


class Application:
    def __init__(self, player: Player) -> None:
        self.app = QApplication([])
        self.window = Window()

        self.form = Form()

        self.form.setupUi(self.window)

        self.player = player

        self.open_map_btn = self.window.findChild(QPushButton, "openMapBtn")
        self.open_map_btn.clicked.connect(self.initMap)

        self.resources_table = self.window.findChild(QTableWidget, "resourceTable")
        self.board = self.window.findChild(QTextEdit, "board")

        self.reporter = Reporter(self.board)
        self.map_window = None

    def initMap(self) -> None:
        self.map_window = MapWindow()
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygameLoop)
        self.timer.start(0)

    def pygameLoop(self) -> None:
        if self.map_window.loop():
            # get result after missions
            pass
            # self.window.close()

    def start(self) -> None:
        self.reporter.post("Вы прибыли на ферму")

        self.window.show()
        self.app.exec_()


def main():
    p = Player()
    app = Application(p)
    app.start()


if __name__ == "__main__":
    main()
