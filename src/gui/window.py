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
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QAction, QComboBox, QDialog, QProgressBar, QTextBrowser, QGridLayout, QWidget
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


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
        self.mainLayout.addWidget(self.takePhotoBtn, 0, 10, 1, 2)

    def initProbabilities(self):
        label = QLabel('Letter Probabilties')
        self.mainLayout.addWidget(label, 1, 10, 1, 2)
        self.mainLayout.addWidget(QTextBrowser(), 2, 10, 8, 2)

    def initCamera(self):
        self.mainLayout.addWidget(QTextBrowser(), 0, 0, 10, 10)

    # Show the dialog
    def trainModel(self):
        dlg = TrainDialog(self)
        dlg.exec()


class TrainDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Download MNIST and Model Training")
        self.setFixedSize(300, 400)  # TODO Fix size

        # Text edit
        self.textBrowserTrain = QTextBrowser(self)
        self.textBrowserTrain.resize(290, 320)
        self.textBrowserTrain.move(5, 5)

        # Progress Bar
        self.pbar = QProgressBar(self)
        self.pbar.resize(290, 30)
        self.pbar.move(5, 335)

        # Combo button
        self.comboBtn = QComboBox(self)
        self.comboBtn.move(5, 375)
        self.comboBtn.resize(90, 20)
        itemsList = ["Model", "MNIST", "OTHER", "HAND AI"]
        self.comboBtn.addItems(itemsList)
        self.comboBtn.show()

        # Train Button
        self.train_btn = QPushButton('Train', self)
        self.train_btn.resize(95, 20)
        self.train_btn.move(100, 375)
        # self.train_btn.clicked.connect(self.train_dataset)  # Train the dataset

        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 375)
        self.cancel_btn.clicked.connect(self.close)


class viewDialog(QDialog):
    # Dialog to view the images
    def __init__(self, parent=None):
        pass
