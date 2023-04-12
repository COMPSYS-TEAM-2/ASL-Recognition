from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from neuralnet.network import Network


class Signals(QObject):
    progress = pyqtSignal(int)
    message = pyqtSignal(str)
    finished = pyqtSignal()


class TrainWorker(QRunnable):

    def __init__(self, network: Network, model: str):
        super().__init__()
        self.network = network
        self.model = model
        self.signals = Signals()

    @pyqtSlot()
    def run(self):
        try:
            self.network.train(
                self.model, self.signals.progress, self.signals.message)
        except StopIteration:
            pass
        finally:
            self.signals.finished.emit()
