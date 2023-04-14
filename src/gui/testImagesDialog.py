from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QScrollArea, QFormLayout, QGroupBox, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QCoreApplication
import pandas as pd
import numpy as np
import PIL.Image as pil
from PIL.ImageQt import ImageQt


class TestImagesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("View Testing Images")
        self.setGeometry(0, 0, 350, 500)
        self.mainLayout = QGridLayout()
        self.scrollArea = QScrollArea(widgetResizable=True)
        self.scrollLayout = QFormLayout()
        self.inputBoxLabel = QLabel("Filter")
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.lineEditChanged)
        self.currentFilter = ""
        self.mainLayout.addWidget(self.inputBoxLabel)
        self.mainLayout.addWidget(self.lineEdit)

        groupBox = QGroupBox()
        groupBox.setLayout(self.scrollLayout)

        self.scrollArea.setWidget(groupBox)
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)
        self.show()

        self.closeEvent = self.exitWindow

        self._iter = iter(range(10000))
        self._timer = QTimer(interval=30, timeout=self.dynamic_loading)
        self._timer.start()

    def dynamic_loading(self):
        try:
            i = next(self._iter)
        except StopIteration:
            self._timer.stop()
        else:
            alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                        "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            data = pd.read_csv('./data/sign_mnist_test/sign_mnist_test.csv')
            w = 28
            h = 28

            for i in range(i):
                if alphabet[int(data["label"].iloc[i])] == self.currentFilter or self.currentFilter == "":
                    QCoreApplication.processEvents()
                    sample = np.reshape(
                        data[data.columns[1:]].iloc[i].values/255, (w, h))
                    img = pil.fromarray(np.uint8(sample*255), 'L')
                    qimg = ImageQt(img)
                    qPixMap = QPixmap.fromImage(qimg).scaled(2*w, 2*h)
                    qPixMapLabel = QLabel()
                    qPixMapLabel.setPixmap(qPixMap)
                    self.scrollLayout.addRow(qPixMapLabel)
                    nameLabel = QLabel(alphabet[int(data["label"].iloc[i])])
                    self.scrollLayout.addRow(nameLabel)

    def exitWindow(self, event):
        self.stopTimer()

    def stopTimer(self):
        self._timer.stop()

    def lineEditChanged(self, text):
        self.stopTimer()
        # When the line edit is changed I need to take the value and refresh the whole window.
        self.currentFilter = text
        self.clearWindow()
        self._iter = iter(range(10000))
        self._timer = QTimer(interval=30, timeout=self.dynamic_loading)
        self._timer.start()

    def clearWindow(self):
        # Clear the window
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().setParent(None)
