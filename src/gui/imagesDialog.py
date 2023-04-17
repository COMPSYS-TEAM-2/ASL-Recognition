from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QScrollArea, QFormLayout, QGroupBox, QLineEdit, QTextBrowser, QCheckBox, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QCoreApplication
import pandas as pd
import numpy as np
import PIL.Image as pil
from PIL.ImageQt import ImageQt


class ImagesDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None, test=False):
        super().__init__(parent=parent)
        self.setGeometry(0, 0, 500, 510)

        if test:
            self.setWindowTitle("Test Images")
            self.data = pd.read_csv('./data/sign_mnist_test.csv')
        else:
            self.setWindowTitle("Train Images")
            self.data = pd.read_csv('./data/sign_mnist_train.csv')

        self.mainLayout = QGridLayout()
        self.scrollArea = QScrollArea(widgetResizable=True)
        self.scrollLayout = QFormLayout()
        self.inputBoxLabel = QLabel("Filter")
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.lineEditChanged)
        self.currentFilter = ""
        self.quantityLabel = QLabel("Quantities")
        self.quantities = QTextBrowser()
        self.quantities.setText(
            "A:\nB:\nC:\nD:\nE:\nF:\nG:\nH:\nI:\nJ:\nK:\nL:\nM:\nN:\nO:\nP:\nQ:\nR:\nS:\nT:\nU:\nV:\nW:\nX:\nY:\nZ:")
        self.letterQuantities = [0]*26

        self.initTestButton()

        self.mainLayout.addWidget(self.inputBoxLabel, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.lineEdit, 1, 0, 1, 6)
        self.mainLayout.addWidget(self.quantityLabel, 1, 6, 1, 2)
        self.mainLayout.addWidget(self.scrollArea, 2, 0, 20, 6)
        self.mainLayout.addWidget(self.quantities, 2, 6, 20, 2)

        groupBox = QGroupBox()
        groupBox.setLayout(self.scrollLayout)

        self.scrollArea.setWidget(groupBox)
        self.setLayout(self.mainLayout)

        self.show()

        self.closeEvent = self.exitWindow
        self.i = 0
        self.selection = []
        self._timer = QTimer(interval=1, timeout=self.dynamic_loading)
        self._timer.start()

    def initTestButton(self):
        self.testButton = QPushButton("Test")
        self.testButton.clicked.connect(self.test)
        self.mainLayout.addWidget(self.testButton, 0, 6, 1, 2)

    def dynamic_loading(self):
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        w = 28
        h = 28
        i = self.i
        self.clear = False

        self.letterQuantities[int(self.data["label"].iloc[i])] += 1
        self.updateTextBrowser(alphabet)

        if alphabet[int(self.data["label"].iloc[i])] == self.currentFilter or self.currentFilter == "":
            # Update text browser
            QCoreApplication.processEvents()
            sample = np.reshape(
                self.data[self.data.columns[1:]].iloc[i].values, (w, h))
            img = pil.fromarray(np.uint8(sample), 'L')
            qimg = ImageQt(img)
            qPixMap = QPixmap.fromImage(qimg).scaled(4*w, 4*h)
            qPixMapLabel = QLabel()
            qPixMapLabel.setPixmap(qPixMap)
            nameLabel = QLabel(alphabet[int(self.data['label'].iloc[i])])

            checkbox = QCheckBox()
            checkbox.clicked.connect(
                lambda bool: self.updateSelection(i, bool))

            if not self.clear:
                self.scrollLayout.addRow(qPixMapLabel)
                self.scrollLayout.addRow(nameLabel)
                self.scrollLayout.addRow(checkbox)

        self.i += 1

    def exitWindow(self, event):
        self.stopTimer()
        event.accept()

    def stopTimer(self):
        self._timer.stop()

    def lineEditChanged(self, text):
        self.stopTimer()
        # When the line edit is changed I need to take the value and refresh the whole window.
        self.currentFilter = text
        self.clearWindow()
        self._timer.start()

    def clearWindow(self):
        self.letterQuantities = [0]*26
        self.i = 0
        # Clear the window
        self.clear = True
        self.selection = []
        for i in range(self.scrollLayout.count()):
            wigit = self.scrollLayout.itemAt(0).widget()
            wigit.setParent(None)
            wigit.destroy()

    def updateTextBrowser(self, letters):
        self.quantities.clear()
        for i, letter in enumerate(letters):
            appendString = str(letter + ": " + str(self.letterQuantities[i]))
            self.quantities.append(appendString)

    def updateSelection(self, index: int, bool: bool):
        if bool:
            if self.selection.count(index) == 0:
                self.selection.append(index)
        else:
            if self.selection.count(index) > 0:
                self.selection.remove(index)

    def test(self):
        print(self.selection)
