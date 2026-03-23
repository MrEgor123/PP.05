from PyQt5 import QtWidgets
from config import APP_COMPANY_NAME, APP_NAME
from db.users_repo import UsersRepo
from ui.admin_window import AdminWindow
from ui.puzzle_widget import PuzzleWidget
from ui.user_window import UserWindow


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.user_repo = UsersRepo()
        self.next_window = None

        self.setWindowTitle(f"{APP_COMPANY_NAME} — {APP_NAME} — Авторизация")
        self.setMinimumSize(420, 520)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.form_layout = QtWidgets.QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        self.login_edit = QtWidgets.QLineEdit()
        self.login_edit.setPlaceholderText("Введите логин")

        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setPlaceholderText("Введите пароль")

        self.form_layout.addRow("Логин", self.login_edit)
        self.form_layout.addRow("Пароль", self.password_edit)

        self.puzzle_widget = PuzzleWidget()
        self.main_layout.addWidget(self.puzzle_widget)

        self.login_button = QtWidgets.QPushButton("Вход")
        self.login_button.clicked.connect(self.login_user)
        self.main_layout.addWidget(self.login_button)

        self.login_edit.setTabOrder(self.login_edit, self.password_edit)
        self.password_edit.setTabOrder(self.password_edit, self.login_button)

    def login_user(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text()

        if login == "" or password == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Поля «Логин» и «Пароль» обязательны для заполнения"
            )
            return

        try:
            user = self.user_repo.get_by_login(login)
        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка работы с базой данных.\n\n{error}"
            )
            return

        if user is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные"
            )
            self.password_edit.clear()
            self.puzzle_widget.shuffle()
            return

        user_id, db_login, db_password, role, login_attempts, is_blocked = user

        if is_blocked:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Вы заблокированы. Обратитесь к администратору"
            )
            self.password_edit.clear()
            return

        if not self.puzzle_widget.is_solved():
            try:
                self.user_repo.fail(user_id)
            except Exception as error:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Ошибка работы с базой данных.\n\n{error}"
                )
                return

            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные"
            )
            self.password_edit.clear()
            self.puzzle_widget.shuffle()
            return

        if password != db_password:
            try:
                self.user_repo.fail(user_id)
            except Exception as error:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Ошибка работы с базой данных.\n\n{error}"
                )
                return

            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные"
            )
            self.password_edit.clear()
            self.puzzle_widget.shuffle()
            return

        try:
            self.user_repo.reset_attempts(user_id)
        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка работы с базой данных.\n\n{error}"
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Информация",
            "Вы успешно авторизовались"
        )

        if role == "admin":
            self.next_window = AdminWindow()
        else:
            self.next_window = UserWindow(login)

        self.next_window.show()
        self.close()