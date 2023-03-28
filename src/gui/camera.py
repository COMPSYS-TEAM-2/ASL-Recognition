from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget
from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


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
        # getting available cameras
        self.availableCameras = QCameraInfo.availableCameras()

        # if no camera found
        if not self.availableCameras:
            label = QLabel('No Camera Detected')
            self.layout().addWidget(label, 1, 1, Qt.AlignmentFlag.AlignCenter)
            return

        self.viewfinder = QCameraViewfinder(self)
        self.layout().addWidget(self.viewfinder, 1, 1, Qt.AlignmentFlag.AlignCenter)

    # method to select camera
    def select_camera(self, i):

        # getting the selected camera
        self.camera = QCamera(self.availableCameras[i])

        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureMode.CaptureStillImage)

        # if any error occur show the alert
        self.camera.error.connect(
            lambda: self.alert(self.camera.errorString()))

        # start the camera
        self.camera.start()

        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)

        # getting current camera name
        self.current_camera_name = self.availableCameras[i]

        # initial save sequence
        self.save_seq = 0
