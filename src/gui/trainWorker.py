from PyQt6.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from neuralnet.train import Train


class Signals(QObject):
    progress = pyqtSignal(int)
    message = pyqtSignal(str)
    timer = pyqtSignal(float)
    finished = pyqtSignal()


class TrainWorker(QRunnable):
    def __init__(self, train: Train, model: str, epoch: int, batch_size: int, split: int, name: str):
        """
        Initialises a new TrainWorker instance which trains the model with the given parameters on a seperate thread.
        """
        super().__init__()
        self.train = train
        self.model = model
        self.signals = Signals()
        self.epoch = epoch
        self.batch_size = batch_size
        self.split = split
        self.name = name

    @pyqtSlot()
    def run(self):
        """
        Runs the training on a seperate thread when the QThreadPool starts the worker.
        """
        try:
            self.train.train(
                self.model, self.name, self.signals.progress, self.signals.message, self.signals.timer, self.epoch, self.batch_size, self.split)
        except StopIteration:
            pass
        finally:
            self.signals.finished.emit()
