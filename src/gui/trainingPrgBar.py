import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QDialog, QLabel, QGridLayout, QProgressBar
from PyQt6.QtCore import Qt


class TrainingPrgBar(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Training Progress...")

        self.mainLayout = QGridLayout()

        self.progBar = QProgressBar()
        self.mainLayout.addWidget(
            self.progBar, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        self.mainLayout.addWidget(
            self.cancelButton, 1, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)
        self.show()

 

        