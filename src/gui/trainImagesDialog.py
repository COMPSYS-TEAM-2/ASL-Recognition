from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QScrollArea, QFormLayout, QGroupBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QCoreApplication
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as pil
from PIL.ImageQt import ImageQt


class TrainImagesDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("View Training Images")
        self.setGeometry(0, 0, 350, 500)
        self.scrollArea = QScrollArea(widgetResizable=True)
        self.scrollLayout = QFormLayout()
        groupBox = QGroupBox()
        groupBox.setLayout(self.scrollLayout)

        self.scrollArea.setWidget(groupBox)
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)
        self.show()

        self.closeEvent = self.dialogClosed

        self._iter = iter(range(10000))
        # Splitting image set into intervals of 1000
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
            data = pd.read_csv('./data/sign_mnist_train/sign_mnist_train.csv')
            w = 28
            h = 28

            for i in range(i):
                QCoreApplication.processEvents()
                sample = np.reshape(
                    data[data.columns[1:]].iloc[i].values/255, (w, h))
                img = pil.fromarray(np.uint8(sample*255), 'L')
                # qImg = QImage(sample.data, w, h, w,
                #               QImage.Format.Format_Grayscale8)
                qimg = ImageQt(img)
                # qPixMap = QPixmap.fromImage(qImg.scaled(10*w, 10*h))
                qPixMap = QPixmap.fromImage(qimg).scaled(2*w, 2*h)
                qPixMapLabel = QLabel()
                qPixMapLabel.setPixmap(qPixMap)
                self.scrollLayout.addRow(qPixMapLabel)
                nameLabel = QLabel(alphabet[int(data["label"].iloc[i])])
                self.scrollLayout.addRow(nameLabel)

    def dialogClosed(self, event):
        self._timer.stop()
