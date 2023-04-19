from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QScrollArea, QFormLayout, QGroupBox, QLineEdit, QTextBrowser, QCheckBox, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
import numpy as np
import PIL.Image as pil
from PIL.ImageQt import ImageQt
from neuralnet.data import Data

from neuralnet.mnist import MNIST


class ImagesDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None, test=False):
        """
        Initializes the image viewing dialog.
        """
        super().__init__(parent=parent)
        self.setGeometry(0, 0, 500, 510)

        if test:
            self.setWindowTitle("Test Images")
            self.data = Data().test_data
        else:
            self.setWindowTitle("Train Images")
            self.data = Data().train_data

        self.letterQuantities = self.data.iloc[:, 0].value_counts(sort=False)

        self.initConstants()
        self.initLayout()
        self.initImageViewer()
        self.initFilter()
        self.initQuantities()
        self.initTestButton()
        self.show()

        self.closeEvent = self.exitWindow
        self.i = 0
        self.selection = []
        self._timer = QTimer(interval=1, timeout=self.dynamicLoading)
        self._timer.start()

    def initLayout(self):
        """
        Initializes the layout of the dialog.
        """
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

    def initFilter(self):
        """
        Initializes the filter input box.
        """
        self.inputBoxLabel = QLabel("Filter")
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.lineEditChanged)
        self.currentFilter = ""
        self.mainLayout.addWidget(self.inputBoxLabel, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.lineEdit, 1, 0, 1, 6)

    def initQuantities(self):
        """
        Initializes the quantities text browser.
        """
        self.quantityLabel = QLabel("Quantities")
        self.quantities = QTextBrowser()
        for i, letter in enumerate(self.alphabet):
            try:
                count = self.letterQuantities[i]
            except KeyError:
                count = 0
            appendString = str(f"{letter}: {count}")
            self.quantities.append(appendString)
        self.letterQuantities = [0]*26
        self.mainLayout.addWidget(self.quantityLabel, 1, 6, 1, 2)
        self.mainLayout.addWidget(self.quantities, 2, 6, 20, 2)

    def initImageViewer(self):
        """
        Initializes the image viewer.
        """
        self.scrollArea = QScrollArea(widgetResizable=True)
        self.scrollLayout = QFormLayout()
        groupBox = QGroupBox()
        groupBox.setLayout(self.scrollLayout)
        self.scrollArea.setWidget(groupBox)
        self.mainLayout.addWidget(self.scrollArea, 2, 0, 20, 6)

    def initTestButton(self):
        """
        Initializes the test button.
        """
        self.testButton = QPushButton("Test")
        self.testButton.clicked.connect(self.test)
        self.mainLayout.addWidget(self.testButton, 0, 6, 1, 2)

    def initConstants(self):
        """
        Initializes the constants.
        """
        self.w = 28
        self.h = 28
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def dynamicLoading(self):
        """
        Loads one image from the dataset.
        """
        if (self.i >= len(self.data)):
            self.stopTimer()
            return

        i = self.i
        self.clear = False

        # If the letter of the image is not the same as the fileter, skip it
        if self.currentFilter.upper().find(self.alphabet[int(self.data.iloc[i, 0])]) != -1 or self.currentFilter == "":
            # Format the image to be used by PyQt
            sample = np.reshape(
                self.data.iloc[i, 1:].values, (self.w, self.h))
            img = pil.fromarray(np.uint8(sample), 'L')
            qimg = ImageQt(img)
            qPixMap = QPixmap.fromImage(qimg).scaled(4*self.w, 4*self.h)
            qPixMapLabel = QLabel()
            qPixMapLabel.setPixmap(qPixMap)
            nameLabel = QLabel(self.alphabet[int(self.data.iloc[i, 0])])

            checkbox = QCheckBox()
            checkbox.clicked.connect(
                lambda bool: self.updateSelection(i, bool))

            if not self.clear:
                self.scrollLayout.addRow(qPixMapLabel)
                self.scrollLayout.addRow(nameLabel)
                self.scrollLayout.addRow(checkbox)

        self.i += 1

    def exitWindow(self, event):
        """
        Exit the window.
        """
        self.stopTimer()
        event.accept()

    def stopTimer(self):
        """
        Stops the timer stopping loading images.
        """
        self._timer.stop()

    def lineEditChanged(self, text):
        """
        Updates the filter when the line edit is changed.
        """
        self.stopTimer()
        # When the line edit is changed I need to take the value and refresh the whole window.
        self.currentFilter = text
        self.clearWindow()
        self._timer.start()

    def clearWindow(self):
        """
        Clears the images and resets the selection and index.
        """
        self.letterQuantities = [0]*26
        self.i = 0
        # Clear the window
        self.clear = True
        self.selection = []
        for i in range(self.scrollLayout.count()):
            wigit = self.scrollLayout.itemAt(0).widget()
            wigit.setParent(None)
            wigit.destroy()

    def updateSelection(self, index: int, bool: bool):
        """
        Updates the selection list.
        """
        if bool:
            if self.selection.count(index) == 0:
                self.selection.append(index)
        else:
            if self.selection.count(index) > 0:
                self.selection.remove(index)

    def test(self):
        """
        Tests the selected images.
        """
        window = self.parent()
        if (not len(self.selection)):
            window.messageDialog(
                "Error!", "No images were selected to test.")
            return
        try:
            # Load the model
            window.loadModel()
            # Select the images selected by the user
            images = self.data.iloc[self.selection]
            # Format the images to be used by the network and test them
            images = MNIST(images)
            correct, total = window.test.test_all(images, False)
            window.messageDialog(
                "Results", f"{correct}/{total} images were correctly classified.")
        except:
            window.messageDialog(
                "Error!", "Unable to find model")
