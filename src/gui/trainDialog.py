# Therefore the initial window should have buttons to import data or view the dataset
from PyQt6.QtWidgets import QDialog, QProgressBar, QPushButton


class TrainDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Model Training")
        self.setFixedSize(300, 40)  # TODO Fix size

        # Progress Bar
        self.pbar = QProgressBar(self)
        self.pbar.resize(290, 30)
        self.pbar.move(5, 5)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)
        self.pbar.show()

        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 50)
        self.cancel_btn.clicked.connect(self.close)

    def setThread(self, thread):
        self.thread = thread

    def closeEvent(self, event):
        self.thread.terminate()
        event.accept()
