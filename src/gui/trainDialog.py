import datetime
from PyQt6.QtWidgets import QDialog, QTextBrowser, QProgressBar, QPushButton
from PyQt6.QtCore import QTimer


class TrainDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        """
        Initializes the training dialog
        """
        super().__init__(parent=parent)
        self.setWindowTitle("Training")
        self.setFixedSize(300, 400)  # TODO Fix size
        self.time_remaning = -1
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

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.time = QTextBrowser(self)
        self.time.resize(95, 27)
        self.time.move(5, 370)
        self.time.setText("--:--:--")

        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 375)
        self.cancel_btn.clicked.connect(self.close)
        self.show()

    def setCancelFunc(self, cancelFunc):
        """
        Sets the cancel function allowing the user to cancel the training process
        """
        self.cancelFunc = cancelFunc

    def setTime(self, time):
        """
        Sets the time remaining to time
        """
        if self.time_remaning == -1:
            self.timer.start(1000)
        self.time_remaning = int(time)
        self.updateGUI()

    def updateTime(self):
        """
        On time out, updates the time remaining
        """
        self.time_remaning -= 1
        if self.time_remaning <= 0:
            self.time_remaning = 0
            self.timer.stop()
        self.updateGUI()

    def updateGUI(self):
        """
        Updates the time remaining to the GUI
        """
        self.time_remaning
        self.time.setText(str(datetime.timedelta(seconds=self.time_remaning)))

    def closeEvent(self, event):
        """
        On close of the dialog, stops the timer and calls the Network cancel function
        """
        self.cancelFunc()
        self.timer.stop()
        event.accept()
