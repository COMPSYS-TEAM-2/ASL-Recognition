import datetime
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
        print("bind")

    def _takePhoto(self):
        print("Click")
        image = QImage()
        id = self._window.captureSession.imageCapture().capture()
        self._window.captureSession.imageCapture().imageCaptured.emit(id, image)
        print(id, image)
        print(image.save("../output/test", "png", 100))


        