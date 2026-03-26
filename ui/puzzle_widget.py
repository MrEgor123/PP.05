from random import shuffle
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget


class PuzzleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.correct = [0, 1, 2, 3]
        self.current = [0, 1, 2, 3]
        self.first = None

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QtWidgets.QLabel("Соберите изображение")
        self.layout.addWidget(self.title_label)

        self.grid = QtWidgets.QGridLayout()
        self.layout.addLayout(self.grid)

        self.buttons = []

        for i in range(4):
            button = QtWidgets.QPushButton()
            button.setFixedSize(100, 100)
            button.setIconSize(button.size())
            button.clicked.connect(lambda _, index=i: self.click_piece(index))
            self.grid.addWidget(button, i // 2, i % 2)
            self.buttons.append(button)

        self.shuffle()

    def count_correct_positions(self):
        return sum(1 for i, piece in enumerate(self.current) if piece == self.correct[i])

    def shuffle(self):
        self.current = self.correct.copy()

        while True:
            shuffle(self.current)
            if self.current != self.correct and self.count_correct_positions() <= 1:
                break

        self.first = None
        self.draw()

    def draw(self):
        for i, piece in enumerate(self.current):
            self.buttons[i].setIcon(QIcon(f"assets/captcha/{piece}.png"))

    def click_piece(self, index):
        if self.first is None:
            self.first = index
            return

        self.current[self.first], self.current[index] = self.current[index], self.current[self.first]
        self.first = None
        self.draw()

    def is_solved(self):
        return self.current == self.correct