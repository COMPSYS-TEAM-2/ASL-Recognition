from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTextBrowser, QGridLayout, QWidget, QComboBox, QSlider
from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtGui import QAction
from gui.camera import Camera
from gui.errorDialog import ErrorDialog
from gui.imagesDialog import ImagesDialog
from gui.trainConfig import TrainConfig
from neuralnet.network import Network


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Define the initial setup
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(0, 0, 1280, 720)

        self.threadpool = QThreadPool()
        self.network = Network()
        self.network.setSaveMethod(self.saveModel)

        self.loadModels()

        self.initMainLayout()
        self.initTitle()
        self.initMenubar()
        self.initCamera()
        self.initButton()
        self.initModelSelector()
        self.initInfo()
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
        self.font.setPointSize(36)
        self.font.setBold(0)
        self.title.setFont(self.font)
        self.mainLayout.addWidget(
            self.title, 0, 10, 2, 2, Qt.AlignmentFlag.AlignCenter)

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
            self.takePhotoBtn, 2, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.takePhotoBtn.clicked.connect(self.camera.takePhoto)
        if (self.camera.availableCameras):
            self.camera.captureSession.imageCapture(
            ).imageCaptured.connect(self.camera.handleCapture)

    def initModelSelector(self):
        # Combo button
        self.modelsBox = QComboBox(self)
        self.modelsBox.addItems(self.models)
        self.mainLayout.addWidget(
            self.modelsBox, 3, 10, 1, 2, Qt.AlignmentFlag.AlignTop)
        self.modelsBox.currentTextChanged.connect(self.updateModelInfo)

    def initInfo(self):
        self.modelLabel = QLabel('Model:')
        self.mainLayout.addWidget(
            self.modelLabel, 4, 10, 1, 1, Qt.AlignmentFlag.AlignTop)
        self.epochLabel = QLabel('Epoch:')
        self.mainLayout.addWidget(
            self.epochLabel, 4, 11, 1, 1, Qt.AlignmentFlag.AlignTop)
        self.batchLabel = QLabel('Batch:')
        self.mainLayout.addWidget(
            self.batchLabel, 4, 10, 1, 1, Qt.AlignmentFlag.AlignBottom)
        self.splitLabel = QLabel('Split:')
        self.mainLayout.addWidget(
            self.splitLabel, 4, 11, 1, 1, Qt.AlignmentFlag.AlignBottom)
        self.updateModelInfo(self.modelsBox.currentText())

    def updateModelInfo(self, name):
        if not name:
            return
        self.modelLabel.setText(f"Model: {self.models[name]['model']}")
        self.epochLabel.setText(f"Epoch: {self.models[name]['epoch']}")
        self.batchLabel.setText(f"Batch: {self.models[name]['batchSize']}")
        self.splitLabel.setText(f"Split: {self.models[name]['split']}%")

    def initProbabilities(self):
        label = QLabel('Letter Probabilties:')
        self.probabilities = QTextBrowser()
        self.probabilities.setText(
            "A:\nB:\nC:\nD:\nE:\nF:\nG:\nH:\nI:\nJ:\nK:\nL:\nM:\nN:\nO:\nP:\nQ:\nR:\nS:\nT:\nU:\nV:\nW:\nX:\nY:\nZ:")
        self.probabilities.append("\n\n<H1>Result:</H1>")
        self.mainLayout.addWidget(
            label, 5, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.mainLayout.addWidget(self.probabilities, 6, 10, 16, 2)

    def initCamera(self):
        self.camera = Camera(self)
        self.mainLayout.addWidget(self.camera, 0, 0, 22, 10)

    def getModel(self):
        # Fetch the value from the combo button
        return self.modelsBox.currentText()

    def errorPopup(self, message):
        ErrorDialog(message, self)

    def train(self):
        TrainConfig(self)

    def showTrainImages(self):
        ImagesDialog(self)

    def showTestImages(self):
        ImagesDialog(self, True)

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

    def loadModels(self):
        self.models = {}
        try:
            f = open("./output/models.sav", 'r')
            lines = f.read().split("\n")
            for line in lines:
                if len(line) == 0:
                    continue
                name, model, epoch, batchSize, split = line.split(",")
                self.updateModel(name, model, epoch, batchSize, split)
            f.close()
        except FileNotFoundError:
            pass

    def updateModel(self, name, model, epoch, batchSize, split):
        self.models[name] = {
            "model": model, "epoch": epoch, "batchSize": batchSize, "split": split}

    def saveModel(self, name, model, epoch, batchSize, split):
        self.updateModel(name, model, epoch, batchSize, split)
        self.modelsBox.removeItem(self.modelsBox.findText(name))
        self.modelsBox.addItem(name)
        f = open("./output/models.sav", 'w')
        for key, value in self.models.items():
            f.write(
                f"{key},{value['model']},{value['epoch']},{value['batchSize']},{value['split']}\n")
        f.close()
