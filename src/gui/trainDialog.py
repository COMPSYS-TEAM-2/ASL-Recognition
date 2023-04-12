# Therefore the initial window should have buttons to import data or view the dataset
from PyQt6.QtWidgets import QDialog, QProgressBar, QPushButton
from PyQt6.QtWidgets import QDialog, QTextBrowser, QProgressBar, QPushButton


class TrainDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Download MNIST and Model Training")
        self.setFixedSize(300, 400)  # TODO Fix size

        # Text edit
        self.textBrowserTrain = QTextBrowser(self)
        self.textBrowserTrain.resize(290, 320)
        self.textBrowserTrain.move(5, 5)

        # Progress Bar
        self.pbar = QProgressBar(self)
        self.pbar.resize(290, 30)
        self.pbar.move(5, 335)
        self.pbar.setMaximum(100)
        self.pbar.setValue(0)

        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 375)
        self.cancel_btn.clicked.connect(self.close)
        self.show()

    def setCancelFunc(self, cancelFunc):
        self.cancelFunc = cancelFunc

    def closeEvent(self, event):
        self.cancelFunc()
        event.accept()
