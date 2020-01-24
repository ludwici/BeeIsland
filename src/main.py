from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QTableWidget, QTextEdit, QWidget, QGraphicsView, QDoubleSpinBox

from src.MapView import MapView
from src.Player import Player
from src.Reporter import Reporter

Form, Window = uic.loadUiType("main_form.ui")


class Application:
    def __init__(self, player: Player):
        self.app = QApplication([])
        self.window = Window()

        self.map_view = MapView(self.window)
        self.map_view.setMaximumWidth(761)
        self.map_view.setPhoto(QPixmap("../res/images/map1.jpg"))
        self.form = Form()

        self.form.setupUi(self.window)

        self.player = player

        self.resources_table = self.window.findChild(QTableWidget, "resourceTable")
        self.board = self.window.findChild(QTextEdit, "board")
        self.map_tap = self.window.findChild(QWidget, "MapTab")
        self.zoom_factor = self.window.findChild(QDoubleSpinBox, "zoomFactor")
        self.zoom_factor.setValue(self.map_view.zoom)
        self.map_view.zoom_spinbox = self.zoom_factor

        self.map_tap.layout().addWidget(self.map_view)

        self.reporter = Reporter(self.board)

    def start(self):
        self.reporter.post("Вы прибыли на ферму")

        self.window.show()
        self.app.exec_()


def main():
    p = Player()
    app = Application(p)
    app.start()


if __name__ == "__main__":
    main()
