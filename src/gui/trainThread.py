from PyQt6.QtCore import QThread
from neuralnet.network import Network
from PyQt6.QtWidgets import QTextBrowser, QProgressBar

class TrainThread(QThread):
    def __init__(self, network: Network, model: str, pbar: QProgressBar):
        super().__init__()
        self.network = network
        self.model = model
        self.pbar = pbar

    def run(self):
        # Training the Dataset
        self.network.train(self.model, self.pbar)
        self.exit()
