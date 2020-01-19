from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidget, QTextEdit

from src.Player import Player
from src.Reporter import Reporter

Form, Window = uic.loadUiType("main_form.ui")


class Application:
    def __init__(self, player: Player):
        self.app = QApplication([])
        self.window = Window()
        self.form = Form()

        self.form.setupUi(self.window)

        self.player = player

        self.resources_table = self.window.findChild(QTableWidget, "resourceTable")
        self.board = self.window.findChild(QTextEdit, "board")

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
