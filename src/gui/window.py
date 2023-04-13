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
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTextBrowser, QGridLayout, QWidget, QComboBox,QSlider
from PyQt6.QtCore import Qt,QThreadPool
from PyQt6.QtGui import QAction
from gui.camera import Camera
from gui.errorDialog import ErrorDialog
from gui.trainImagesDialog import TrainImagesDialog
from gui.testImagesDialog import TestImagesDialog
from gui.trainDialog import TrainDialog
from neuralnet.network import Network
from gui.trainWorker import TrainWorker




class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Define the initial setup
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(0, 0, 1280, 720)

        self.threadpool = QThreadPool()
        self.network = Network()

        self.initMainLayout()
        self.initTitle()
        self.initMenubar()
        self.initCamera()
        self.initButton()
       # self.initTrainingSlider() # Could make errors
        self.initModelSelector() #Could make errors
        self.initProbabilities()
      

        self.show()

    def initMainLayout(self):
        self.mainLayout = QGridLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def initTitle(self):
        self.font = self.font()
        self.title = QLabel("HAND AI")
        self.font.setPointSize(64)
        self.font.setBold(0)
        self.title.setFont(self.font)
        self.mainLayout.addWidget(self.title,0,10,1,2,Qt.AlignmentFlag.AlignBottom.AlignCenter)

    def initMenubar(self):
        # Quit Action (File)
        self.exitAct = QAction('&Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.triggered.connect(QApplication.quit)

        # Train Model Action (File)
        self.trainModelAct = QAction('&Train Model', self)
        self.trainModelAct.triggered.connect(self.train)

        # # View Trained Images (View)
        trainImagesAct = QAction('&View Training Images', self)
        trainImagesAct.triggered.connect(self.showTrainImages)

        # # View Test Images (View)
        testImagesAct = QAction('&View Testing Images', self)
        testImagesAct.triggered.connect(self.showTestImages)

        # Menubar
        menubar = self.menuBar()

        # File section
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.trainModelAct)
        fileMenu.addAction(self.exitAct)
        # View section
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(trainImagesAct)
        viewMenu.addAction(testImagesAct)

    def initButton(self):
        self.takePhotoBtn = QPushButton('Take photo')
        self.mainLayout.addWidget(
            self.takePhotoBtn, 2, 10, 1, 2, Qt.AlignmentFlag.AlignTop)
        self.takePhotoBtn.clicked.connect(self.camera.takePhoto)
        if (self.camera.availableCameras):
            self.camera.captureSession.imageCapture(
            ).imageCaptured.connect(self.camera.handleCapture)

    def initModelSelector(self):
        # Combo button
        self.models = QComboBox(self)
        itemsList = ["LeNet", "AlexNet", "ResNet"]
        self.models.addItems(itemsList)
        self.mainLayout.addWidget(
            self.models, 2, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)

    def getComboButtonValue(self):
        # Fetch the value from the combo button
        return str(self.comboBtn.currentText())
    
    def initTrainingSlider(self):

        self.sliderLabel = QLabel("Percentage of Training set to use ?")
        self.mainLayout.addWidget(self.sliderLabel,1,10,1,2,Qt.AlignmentFlag.AlignBottom)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(20)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self.mainLayout.addWidget(self.slider, 2, 10, 1, 2,Qt.AlignmentFlag.AlignBottom)
        self.slider.valueChanged.connect(self.getSliderValue)
        self.pcent = QLabel(str(self.getSliderValue()))
        self.mainLayout.addWidget(self.pcent,2, 12, 1, 1,Qt.AlignmentFlag.AlignBottom)
        

    def getSliderValue(self):
        self.percentage = self.slider.value()
        return self.percentage
    
        

        
    def initProbabilities(self):
        label = QLabel('Letter Probabilties')
        self.probabilities = QTextBrowser()
        self.probabilities.setText(
            "A:\nB:\nC:\nD:\nE:\nF:\nG:\nH:\nI:\nJ:\nK:\nL:\nM:\nN:\nO:\nP:\nQ:\nR:\nS:\nT:\nU:\nV:\nW:\nX:\nY:\nZ:")
        self.probabilities.append("\n\n<H1>Result:</H1>")
        self.mainLayout.addWidget(label, 3, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.mainLayout.addWidget(self.probabilities, 4, 10, 9, 2)
        #self.mainLayout.addWidget(label, 3, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        #self.mainLayout.addWidget(QTextBrowser(), 4, 10, 6, 3)

    def initCamera(self):
        self.camera = Camera(self)
        self.mainLayout.addWidget(self.camera, 0, 0, 10, 10)

    def getModel(self):
        # Fetch the value from the combo button
        return self.models.currentText()

    def errorPopup(self, message):
        ErrorDialog(message, self)

    def train(self):
        dlg = TrainDialog(self)
        worker = TrainWorker(self.network, self.getModel())
        worker.signals.progress.connect(dlg.pbar.setValue)
        worker.signals.message.connect(
            dlg.textBrowserTrain.append)
        dlg.setCancelFunc(self.network.cancel)
        self.threadpool.start(worker)

    def showTrainImages(self):
        TrainImagesDialog(self)

    def showTestImages(self):
        TestImagesDialog(self)

    def updatePercentages(self, results, prediction):
        lettersArray = ["A: ", "B: ", "C: ", "D: ", "E: ", "F: ", "G: ", "H: ", "I: ", "J: ", "K: ", "L: ",
                        "M: ", "N: ", "O: ", "P: ", "Q: ", "R: ", "S: ", "T: ", "U: ", "V: ", "W: ", "X: ", "Y: ", "Z: "]
        valuesArray = []
        # Use a set of for loops to take the results, put them into a dict, print this dict to the text box
        for i in results:
            for j in i:
                # Set j to be my string
                # Remove unwanted characters from the string
                myVal = str(j)
                myVal = myVal.replace("tensor(", "")
                myVal = myVal.replace(", grad_fn=<UnbindBackward0>)", "")
                valuesArray.append(myVal)
        # Insert all of the values into the text box
        self.probabilities.clear()
        for i, letter in enumerate(lettersArray):
            appendString = str(letter + valuesArray[i] + "%")
            self.probabilities.append(appendString)
        appendResultString = str(
            "\n\n<H1>Result: " + chr(prediction + ord('A')) + "</H1>")
        self.probabilities.append(appendResultString)
