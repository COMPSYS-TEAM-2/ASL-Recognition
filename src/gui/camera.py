from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtMultimedia import QMediaDevices, QCamera, QCameraDevice, QMediaCaptureSession, QImageCapture
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QPalette, QColor, QImage
from PyQt6.QtCore import Qt
from torch import max

from image.image import prepareImage


class Camera(QWidget):

    def __init__(self, win):
        super(Camera, self).__init__()
        self.initPalette()
        self.initMainLayout()
        self.initCamera()
        self.win = win

    def initMainLayout(self):
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def initPalette(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("green"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
        self.setPalette(palette)

    def initCamera(self):
        self.availableCameras = QMediaDevices.videoInputs()
        if not self.availableCameras:
            label = QLabel('No Camera Detected')
            self.layout().addWidget(label, 1, 1, Qt.AlignmentFlag.AlignCenter)
            return

        camera = QCamera(self.availableCameras[0], self)
        self.captureSession = QMediaCaptureSession(self)
        self.captureSession.setCamera(camera)

        preview = QVideoWidget(self)
        self.layout().addWidget(preview, 1, 1)

        self.captureSession.setVideoOutput(preview)

        imageCapture = QImageCapture(camera)
        self.captureSession.setImageCapture(imageCapture)

        camera.start()

    def takePhoto(self):
        try:
            self.captureSession.imageCapture().capture()
        except AttributeError:
            self.win.errorPopup("No camera detected")

    def handleCapture(self, id: int, capture: QImage):
        image = prepareImage(capture)
        print(self.predictImage(image))

    def predictImage(self, image):
        try:
            # Load model takes name as an input, set this to be the value from the combobox
            self.win.network.load_model(self.win.getModel())
            result = self.win.network.test(image)
            _, prediction = max(result, 1)
            # Result is an array of all the probablilities
            # This can be passed to the window in order to fill the percentages box
            self.win.updatePercentages(result, prediction)
            return chr(prediction + ord('A'))
        except:
            self.win.errorPopup("Unable to find model")
        return "Error"
