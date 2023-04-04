import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QDialog, QLabel, QGridLayout, QProgressBar
from PyQt6.QtCore import Qt
import time

class Actions(QDialog):

    def __init__(self):
        super().__init__()
        self.showPbar()
        
    def showPbar(self):
        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.button = QPushButton('Start', self)
        self.button.move(0, 30)
        self.show()

        self.button.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        count = 0
        while count < 200:
            count += 1
            time.sleep(1)
            self.progress.setValue(count)
 

        