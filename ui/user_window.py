from PyQt5 import QtWidgets
from config import APP_COMPANY_NAME, APP_NAME


class UserWindow(QtWidgets.QWidget):
    def __init__(self, login, full_name=""):
        super().__init__()

        self.setWindowTitle(f"{APP_COMPANY_NAME} — {APP_NAME} — Пользователь")
        self.setMinimumSize(400, 300)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        if full_name != "":
            text = f"Добро пожаловать, {full_name} ({login})"
        else:
            text = f"Добро пожаловать, {login}"

        self.label = QtWidgets.QLabel(text)
        self.layout.addWidget(self.label)