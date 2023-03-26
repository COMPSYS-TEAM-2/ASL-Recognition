from gui.window import Window
from neuralnet.network import Network


class Controller:
    def __init__(self, window):
        self._network = Network()
        self._window = window
