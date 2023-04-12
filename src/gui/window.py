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
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTextBrowser, QGridLayout, QWidget, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from gui.camera import Camera
from gui.errorDialog import ErrorDialog
from gui.trainImagesDialog import TrainImagesDialog
from gui.testImagesDialog import TestImagesDialog
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
        self.initComboButton()
        self.initProbabilities()

        self.show()

    def initMainLayout(self):
        self.mainLayout = QGridLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def initMenubar(self):
        # Quit Action (File)
        self.exitAct = QAction('&Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.triggered.connect(QApplication.quit)

        # Train Model Action (File)
        self.trainModelAct = QAction('&Train Model', self)

        # # View Trained Images (View)
        trainImagesAct = QAction('&View Training Images', self)
        trainImagesAct.triggered.connect(self.showTrainImages)

        # # View Test Images (View)
        testImagesAct = QAction('&View Testing Images', self)
        testImagesAct.triggered.connect(self.showTestImages)

        # Menubar
        menubar = self.menuBar()

        # File section
        self.fileMenu = menubar.addMenu('&File')

        # View section
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(trainImagesAct)
        viewMenu.addAction(testImagesAct)

    def initButton(self):
        self.takePhotoBtn = QPushButton('Take photo')
        self.mainLayout.addWidget(
            self.takePhotoBtn, 0, 10, 1, 2, Qt.AlignmentFlag.AlignTop)

    def initComboButton(self):
        # Combo button
        self.comboBtn = QComboBox(self)
        itemsList = ["LeNet", "AlexNet", "ResNet"]
        self.comboBtn.addItems(itemsList)
        self.mainLayout.addWidget(
            self.comboBtn, 0, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)

    def getModel(self):
        # Fetch the value from the combo button
        return str(self.comboBtn.currentText())

    def initProbabilities(self):
        label = QLabel('Letter Probabilties')
        self.mainLayout.addWidget(
            label, 1, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.mainLayout.addWidget(QTextBrowser(), 2, 10, 8, 2)

    def initCamera(self):
        self.camera = Camera()
        self.mainLayout.addWidget(self.camera, 0, 0, 10, 10)

    def showTrainImages(self):
        TrainImagesDialog(self)

    def showTestImages(self):
        TestImagesDialog(self)

    def errorMessageDlg(self):
        ErrorDialog(self)

    def trainDialog(self):
        dlg = TrainDialog(self)
        dlg.show()
        return dlg
