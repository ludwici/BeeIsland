from PyQt5.QtWidgets import QTextEdit


class Reporter:
    def __init__(self, board: QTextEdit) -> None:
        self.board = board

    def post(self, text) -> None:
        self.board.append(text)
