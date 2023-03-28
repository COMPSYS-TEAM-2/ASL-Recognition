from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class Camera(QWidget):

    def __init__(self):
        super(Camera, self).__init__()

        self.initPalette()
        self.initMainLayout()

        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # if no camera found
        if not self.available_cameras:
            label = QLabel('No Camera Detected')
            self.layout().addWidget(label, 1, 1, Qt.AlignmentFlag.AlignCenter)
            return

        self.viewfinder = QCameraViewfinder(self)

    def initMainLayout(self):
        self.setLayout(QGridLayout())

    def initPalette(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("black"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
        self.setPalette(palette)
