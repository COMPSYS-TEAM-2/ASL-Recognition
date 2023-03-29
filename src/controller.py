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
        try:
                    id = self._window.camera.captureSession.imageCapture().capture()
                    self._window.camera.captureSession.imageCapture().imageCaptured.connect(lambda: print("test"))
                    print(id)
        except AttributeError:
            print("No Camera")


        