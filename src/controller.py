import datetime
import time
from gui.window import Window
from neuralnet.network import Network
from PyQt6.QtGui import QImage
from PIL import Image
import numpy as np

class Controller:
    def __init__(self):
        self._network = Network()
        self._window = Window()
        self._initButtons()

    def _initButtons(self):
        self._window.takePhotoBtn.clicked.connect(self._takePhoto)
        self._window.camera.captureSession.imageCapture(
        ).imageCaptured.connect(self._handleCapture)

    def _takePhoto(self):
        print("Click")
        try:
                    id = self._window.camera.captureSession.imageCapture().capture()
        except AttributeError:
            print("No Camera")

    def _handleCapture(self, id: int, capture: QImage):
        image = capture.convertToFormat(QImage.Format.Format_RGB32)
        height = image.height()
        width = image.width()
        pointer = image.constBits()
        pointer.setsize(height * width * 4)
        arr = np.frombuffer(pointer, np.uint8).reshape((height, width, 4))
        img = Image.fromarray(arr[..., 2::-1])
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        img.save(f"output/photos/{timestamp}.png")
         
        