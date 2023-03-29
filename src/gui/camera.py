from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtMultimedia import QMediaDevices, QCamera, QCameraDevice, QMediaCaptureSession, QImageCapture
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class Camera(QWidget):

    def __init__(self):
        super(Camera, self).__init__()
        self.initPalette()
        self.initMainLayout()
        self.initCamera()

    def initMainLayout(self):
        self.setLayout(QGridLayout())

    def initPalette(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("black"))
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
        preview.resize(290, 470)
        preview.move(5, 25)
        self.layout().addWidget(preview, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.captureSession.setVideoOutput(preview)

        imageCapture = QImageCapture(camera)
        self.captureSession.setImageCapture(imageCapture)

        camera.start()
