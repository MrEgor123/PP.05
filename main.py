import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)

    try:
        window = LoginWindow()
        window.show()
    except Exception as error:
        QMessageBox.critical(
            None,
            "Ошибка",
            f"Не удалось запустить приложение.\n\n{error}"
        )
        sys.exit(1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()