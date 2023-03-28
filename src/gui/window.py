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
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QAction, QComboBox, QDialog, QProgressBar, QTextBrowser
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Define the initial setup
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(300, 100, 400, 500)
        # Quit Action (File)
        exitAct = QAction('&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(QApplication.quit)

        # Train Model Action (File)
        trainModelAct = QAction('&Train Model', self)
        trainModelAct.triggered.connect(self.trainModel)

        # View Trained Images (View)
        trainImagesAct = QAction('&View Training Images', self)
        # trainImagesAct.triggered.connect(self.showTrainImages)

        # View Test Images (View)
        testImagesAct = QAction('&View Testing Images', self)
        # testImagesAct.triggered.connect(self.showTestImages)

        # Menubar
        menubar = self.menuBar()

        # File section
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(trainModelAct)
        fileMenu.addAction(exitAct)

        # View section
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(trainImagesAct)
        viewMenu.addAction(testImagesAct)

        self.init_btn()
        self.init_probabilities()
        self.init_camera()

        self.show()

    def init_btn(self):
        self.takePhotoBtn = QPushButton('Take photo', self)
        self.takePhotoBtn.resize(95, 20)
        self.takePhotoBtn.move(300, 25)
        self.takePhotoBtn.show()

    def init_probabilities(self):
        label1 = QLabel('Letter Probabilties', self)
        label1.resize(95, 40)
        label1.move(300, 40)
        label1.show()
        self.textBrowserData = QTextBrowser(
            self)  # displaying probability widget
        self.textBrowserData.resize(95, 300)
        self.textBrowserData.move(300, 75)
        self.textBrowserData.show()

    def init_camera(self):
        pass

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
