# For the layout of our pyqt window
# Need to be able to save and load
# Need to be able to download data
# User can import dataset
# User can see time left to finish import
# User can stop the progress
# User can view images of the train or test dataset
# User can scroll up or down to view all the images
# User can filter to see specific images
# User can see simple statistics of the dataset

# Therefore the initial window should have buttons to import data or view the dataset
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QAction,QTextBrowser, QGridLayout, QWidget
from PyQt5.QtCore import Qt

from gui.camera import Camera
from gui.trainDialog import TrainDialog


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Define the initial setup
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(0, 0, 1280, 720)

        self.initMainLayout()
        self.initMenubar()
        self.initCamera()
        self.initButton()
        self.initProbabilities()

        self.show()

    def initMainLayout(self):
        self.mainLayout = QGridLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def initMenubar(self):
        # Quit Action (File)
        exitAct = QAction('&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(QApplication.quit)

        # Train Model Action (File)
        trainModelAct = QAction('&Train Model', self)
        trainModelAct.triggered.connect(self.trainModel)

        # # View Trained Images (View)
        # trainImagesAct = QAction('&View Training Images', self)
        # # trainImagesAct.triggered.connect(self.showTrainImages)

        # # View Test Images (View)
        # testImagesAct = QAction('&View Testing Images', self)
        # # testImagesAct.triggered.connect(self.showTestImages)

        # Menubar
        menubar = self.menuBar()

        # File section
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(trainModelAct)
        fileMenu.addAction(exitAct)

        # View section
        viewMenu = menubar.addMenu('&View')
        # viewMenu.addAction(trainImagesAct)
        # viewMenu.addAction(testImagesAct)

    def initButton(self):
        self.takePhotoBtn = QPushButton('Take photo')
        self.mainLayout.addWidget(
            self.takePhotoBtn, 0, 10, 1, 2, Qt.AlignmentFlag.AlignTop)

    def initProbabilities(self):
        label = QLabel('Letter Probabilties')
        self.mainLayout.addWidget(
            label, 0, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.mainLayout.addWidget(QTextBrowser(), 1, 10, 9, 2)

    def initCamera(self):
        self.mainLayout.addWidget(Camera(), 0, 0, 10, 10)

    # Show the dialog
    def trainModel(self):
        dlg = TrainDialog(self)
        dlg.exec()
