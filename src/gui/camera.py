from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtMultimedia import QMediaDevices, QCamera, QMediaCaptureSession, QImageCapture
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QPalette, QColor, QImage
from PyQt6.QtCore import Qt
from torch import max

from image.image import prepareImage


class Camera(QWidget):
    def __init__(self, win):
        """
        Initializes the camera widget.
        """
        super(Camera, self).__init__()
        self.initPalette()
        self.initMainLayout()
        self.initCamera()
        self.win = win

    def initMainLayout(self):
        """
        Initializes the main layout of the widget.
        """
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def initPalette(self):
        """
        Initializes the palette of the widget.
        """
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("black"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
        self.setPalette(palette)

    def initCamera(self):
        """
        Initializes the camera.
        """
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
        """
        Takes a photo using the camera.
        """
        try:
            self.captureSession.imageCapture().capture()
        except AttributeError:
            self.win.messageDialog("Error!", "No camera detected")

    def handleCapture(self, id: int, capture: QImage):
        """
        On camera capture, this function is called.
        It prepates and predicts the result of the captured image.
        """
        image = prepareImage(capture)
        self.predictImage(image)

    def predictImage(self, image):
        """
        Predicts the image using the loaded model.
        """
        try:
            # Load model takes name as an input, set this to be the value from the combobox
            self.win.loadModel()
            result = self.win.test.test(image)
            _, prediction = max(result, 1)
            # Result is an array of all the probablilities
            # This can be passed to the window in order to fill the percentages box
            self.win.updatePercentages(result, prediction)
        except:
            self.win.messageDialog("Error!", "Unable to find model")
