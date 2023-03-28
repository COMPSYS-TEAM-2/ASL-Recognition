
import sys
from PyQt5.QtWidgets import QApplication
from controller import Controller
from gui.palette import set_palette


def main():
    app = QApplication([])
    set_palette(app)
    _ = Controller()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
