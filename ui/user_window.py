from PyQt5 import QtWidgets
from config import APP_COMPANY_NAME, APP_NAME


class UserWindow(QtWidgets.QWidget):
    def __init__(self, login, full_name=""):
        super().__init__()

        self.login_window = None

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

        self.logout_button = QtWidgets.QPushButton("Выход из учетной записи")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

    def logout(self):
        from ui.login_window import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()