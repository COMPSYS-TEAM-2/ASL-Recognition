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
import PyQt5.QtWidgets as pyqt
from network import Network


class MainWindow(pyqt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Define the initial setup
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(300, 100, 500, 700)
        # self.setWindowIcon(self.QIcon(''))
        self.addMenu()
        # Add to the main page
        self.formLayout = pyqt.QFormLayout()

    # Add the menu

    def addMenu(self):
        menuBar = self.menuBar()
        # Adding menu bar items
        fileMenu = menuBar.addMenu('File')
        dataSetMenu = menuBar.addMenu('Dataset')
        # Add items to the menus
        fileSaveAction = pyqt.QAction("Save", self)
        fileSaveAction.setShortcut('Ctrl+S')
        fileLoadAction = pyqt.QAction("Load", self)
        fileLoadAction.setShortcut('Ctrl+O')
        fileExitAction = pyqt.QAction("Exit", self)
        fileExitAction.setShortcut('Ctrl+Q')
        fileExitAction.triggered.connect(pyqt.qApp.quit)
        dataSetTrain = pyqt.QAction("Train", self)
        dataSetTrain.triggered.connect(self.startTrain)
        dataSetView = pyqt.QAction("View", self)
        dataSetDownload = pyqt.QAction("Download", self)
        # Add actions to dropdowns
        fileMenu.addAction(fileSaveAction)
        fileMenu.addAction(fileLoadAction)
        fileMenu.addAction(fileExitAction)
        dataSetMenu.addAction(dataSetTrain)
        dataSetMenu.addAction(dataSetView)
        dataSetMenu.addAction(dataSetDownload)

    def startTrain(self):
        # Load the new look of the training gui
        self.progress = pyqt.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        self.show()
        network = Network()
        network.load_model()

    def updateProgressBar(self, val1, val2):
        # Update the progress bar to be a percentage of the max training to be completed 5*6400 = 32000
        self.progress.setValue((val1 * val2)/3200)


if (__name__ == '__main__'):
    application = pyqt.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    application.exec()
