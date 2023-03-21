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
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QLabel, QRadioButton, QFormLayout, QLineEdit
from PyQt6.QtGui import *
from network import Network


class MainWindow(QMainWindow):
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
        # trainModelAct.triggered.connect(self.showTrainModel)

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

        self.show()

        self.init_btn()

    def init_btn(self):
        btn = QPushButton('Button', self)
        btn.resize(80, 20)
        btn.move(300, 30)
        btn.show()
        # btn.clicked.connect(self.clear)


if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = MainWindow()
    application.exec()
