import sys
from PyQt6.QtWidgets import QApplication
from gui.palette import setPalette
from gui.window import Window


def main():
    app = QApplication([])
    setPalette(app)
    _ = Window()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
