
from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject


class Signals(QObject):
    error = pyqtSignal()
    finished = pyqtSignal()


class Worker(QRunnable):
    # takes a function as an argument and creates a QRunnable instance
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.signals = Signals()

    @pyqtSlot()
    def run(self):
        try:
            self.function()
            self.signals.finished.emit()
        except:
            self.signals.error.emit()
