from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os


class TrainImagesDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("View Training Images")

        #self.scrollArea = QScrollArea(widgetResizable=True)
        self.mainLayout = QGridLayout()
        # self.mainLayout.addWidget(self.scrollArea)
        self.myPixmap = QPixmap("./data/american_sign_language.PNG")
        self.pixmapLabel = QLabel()
        self.pixmapLabel.setPixmap(self.myPixmap)
        self.mainLayout.addWidget(self.pixmapLabel, 0, 0)
        self.setLayout(self.mainLayout)
        self.show()
