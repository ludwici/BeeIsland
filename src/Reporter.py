from PyQt5.QtWidgets import QTextEdit


class Reporter:
    def __init__(self, board: QTextEdit):
        self.board = board

    def post(self, text):
        self.board.append(text)
