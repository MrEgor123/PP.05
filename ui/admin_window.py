from PyQt5 import QtWidgets
from config import APP_COMPANY_NAME, APP_NAME
from db.users_repo import UsersRepo


class AdminWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.user_repo = UsersRepo()

        self.setWindowTitle(f"{APP_COMPANY_NAME} — {APP_NAME} — Администратор")
        self.setMinimumSize(700, 450)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Логин", "Роль", "Попытки", "Блокировка"]
        )
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.add_button = QtWidgets.QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_user)
        self.buttons_layout.addWidget(self.add_button)

        self.edit_button = QtWidgets.QPushButton("Изменить")
        self.edit_button.clicked.connect(self.edit_user)
        self.buttons_layout.addWidget(self.edit_button)

        self.unblock_button = QtWidgets.QPushButton("Разблокировать")
        self.unblock_button.clicked.connect(self.unblock_user)
        self.buttons_layout.addWidget(self.unblock_button)

        self.update_button = QtWidgets.QPushButton("Обновить")
        self.update_button.clicked.connect(self.load_users)
        self.buttons_layout.addWidget(self.update_button)

        self.load_users()

    def load_users(self):
        try:
            rows = self.user_repo.list_users()
        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка загрузки пользователей.\n\n{error}"
            )
            return

        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            user_id, login, role, login_attempts, is_blocked = row
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(user_id)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(login))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(role))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(login_attempts)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem("Да" if is_blocked else "Нет"))

    def get_selected_user_id(self):
        row = self.table.currentRow()

        if row == -1:
            return None

        return int(self.table.item(row, 0).text())

    def unblock_user(self):
        user_id = self.get_selected_user_id()

        if user_id is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return

        try:
            self.user_repo.unblock_user(user_id)
        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка разблокировки пользователя.\n\n{error}"
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Информация",
            "Пользователь успешно разблокирован"
        )
        self.load_users()

    def add_user(self):
        login, ok = QtWidgets.QInputDialog.getText(
            self,
            "Добавить пользователя",
            "Логин:"
        )

        if not ok:
            return

        login = login.strip()

        if login == "":
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым")
            return

        password, ok = QtWidgets.QInputDialog.getText(
            self,
            "Добавить пользователя",
            "Пароль:"
        )

        if not ok:
            return

        if password == "":
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пароль не может быть пустым")
            return

        role, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Добавить пользователя",
            "Роль:",
            ["admin", "user"],
            0,
            False
        )

        if not ok:
            return

        try:
            if self.user_repo.get_by_login(login) is not None:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Пользователь с указанным логином уже существует"
                )
                return

            self.user_repo.add_user(login, password, role)
        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка добавления пользователя.\n\n{error}"
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Информация",
            "Пользователь успешно добавлен"
        )
        self.load_users()

    def edit_user(self):
        user_id = self.get_selected_user_id()

        if user_id is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return

        login, ok = QtWidgets.QInputDialog.getText(
            self,
            "Изменить пользователя",
            "Логин:"
        )

        if not ok:
            return

        login = login.strip()

        if login == "":
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым")
            return

        password, ok = QtWidgets.QInputDialog.getText(
            self,
            "Изменить пользователя",
            "Пароль:"
        )

        if not ok:
            return

        if password == "":
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пароль не может быть пустым")
            return

        role, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Изменить пользователя",
            "Роль:",
            ["admin", "user"],
            0,
            False
        )

        if not ok:
            return

        try:
            self.user_repo.update_user(user_id, login, password, role)
        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка изменения пользователя.\n\n{error}"
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Информация",
            "Данные пользователя успешно изменены"
        )
        self.load_users()