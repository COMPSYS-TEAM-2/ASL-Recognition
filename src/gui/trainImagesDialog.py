from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os


class TrainImagesDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("View Training Images")

        self.mainLayout = QGridLayout()

        label = QLabel(self)
        pixmap = QPixmap('../../data/american_sign_language.jpg', format='jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        print(pixmap.width(), pixmap.height())
        print(pixmap.isNull())
        print(os.path.exists("../../data/american_sign_language.jpg"))

        self.mainLayout.addWidget(
            label, 0, 0, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)
        self.show()
