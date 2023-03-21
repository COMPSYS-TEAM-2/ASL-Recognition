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
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QLabel, QRadioButton, QFormLayout, QLineEdit, QTextEdit, QComboBox
from PyQt6.QtGui import *
from network import Network


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Define the initial setup
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(300, 100, 400, 600)
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
        self.init_combo_btn()
        self.init_probabilities()

    def init_btn(self):
        btn = QPushButton('Button', self)
        btn.resize(95, 20)
        btn.move(300, 30)
        btn.show()
        # btn.clicked.connect(self.clear)

    def init_combo_btn(self):
        comboBtn = QComboBox(self)
        comboBtn.move(300, 55)
        comboBtn.resize(95, 20)
        itemsList = ["Model", "MNIST", "OTHER", "HAND AI"]
        comboBtn.addItems(itemsList)
        comboBtn.show()

    def init_probabilities(self):
        label1 = QLabel('Letter Probabilties', self)
        label1.resize(95, 40)
        label1.move(300, 180)
        label1.show()
        self.textEdit = QTextEdit(self)  # displaying probability widget
        self.textEdit.resize(95, 300)
        self.textEdit.move(300, 220)
        self.textEdit.show()


if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = MainWindow()
    application.exec()
