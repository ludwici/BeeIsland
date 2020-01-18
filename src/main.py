from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("main_form.ui")


class Application:
    def __init__(self):
        self.app = QApplication([])
        self.window = Window()
        self.form = Form()

        self.form.setupUi(self.window)

    def start(self):
        self.window.show()
        self.app.exec_()


def main():
    app = Application()
    app.start()


if __name__ == "__main__":
    main()
