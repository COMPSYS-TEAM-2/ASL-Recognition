
from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject


class Signals(QObject):
    finished = pyqtSignal()


class Worker(QRunnable):

    def __init__(self, function):
        super().__init__()
        self.function = function
        self.signals = Signals()

    @pyqtSlot()
    def run(self):
        self.function()
        self.signals.finished.emit()
