from PyQt5 import QtWidgets
from config import APP_COMPANY_NAME, APP_NAME


class UserWindow(QtWidgets.QWidget):
    def __init__(self, login):
        super().__init__()

        self.setWindowTitle(f"{APP_COMPANY_NAME} — {APP_NAME} — Пользователь")
        self.setMinimumSize(400, 300)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QtWidgets.QLabel(f"Добро пожаловать, {login}")
        self.layout.addWidget(self.label)