
import sys
from PyQt6.QtWidgets import QApplication
from controller import Controller
from gui.window import Window


def main():
    app = QApplication([])
    window = Window()
    window.show()
    Controller(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
