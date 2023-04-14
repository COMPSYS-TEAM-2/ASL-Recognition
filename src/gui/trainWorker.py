import time
from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from neuralnet.network import Network


class Signals(QObject):
    progress = pyqtSignal(int)
    message = pyqtSignal(str)
    timer = pyqtSignal(float)
    finished = pyqtSignal()


class TrainWorker(QRunnable):

    def __init__(self, network: Network, model: str, epoch: int, batch_size: int, split: int, name: str):
        super().__init__()
        self.network = network
        self.model = model
        self.signals = Signals()
        self.epoch = epoch
        self.batch_size = batch_size
        self.split = split
        self.name = name

    @pyqtSlot()
    def run(self):
        try:
            self.network.train(
                self.model,self.name, self.signals.progress, self.signals.message, self.signals.timer, self.epoch, self.batch_size, self.split)
        except StopIteration:
            pass
        finally:
            self.signals.finished.emit()
