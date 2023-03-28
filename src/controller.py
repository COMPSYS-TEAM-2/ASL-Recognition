import datetime
import time
from gui.window import Window
from neuralnet.network import Network
from PyQt6.QtGui import QImage

class Controller:
    def __init__(self):
        self._network = Network()
        self._window = Window()
        self._initButtons()

    def _initButtons(self):
        self._window.takePhotoBtn.clicked.connect(self._takePhoto)

    def _takePhoto(self):
        print("Click")
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        try:
            self._window.camera.capture.capture(f"output/photos/{timestamp}.jpg")
        except AttributeError:
            print("No Camera")


        