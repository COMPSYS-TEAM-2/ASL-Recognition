
import sys
from PyQt6.QtWidgets import QApplication
from controller import Controller
from gui.window import Window
from gui.palette import set_palette


def main():
    app = QApplication([])
    set_palette(app)
    window = Window()
    Controller(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
