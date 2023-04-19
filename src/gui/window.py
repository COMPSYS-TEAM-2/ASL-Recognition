from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTextBrowser, QGridLayout, QWidget, QComboBox, QFileDialog
from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtGui import QAction
from gui.camera import Camera
from gui.messageDialog import MessageDialog
from gui.imagesDialog import ImagesDialog
from gui.trainConfig import TrainConfig
from gui.worker import Worker
from neuralnet.data import Data
from neuralnet.test import Test


class Window(QMainWindow):
    def __init__(self, parent=None):
        """
        Define the initial setup
        """
        super().__init__(parent)
        self.setWindowTitle("Sign Language Recognition")
        self.setGeometry(0, 0, 1280, 720)

        self.threadpool = QThreadPool()
        self.test = Test()
        # self.network.setSaveMethod(self.saveModel)
        self.data = Data()

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
        """
        Initialize the main layout of the window
        """
        self.mainLayout = QGridLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def initTitle(self):
        """
        Initialize the title of the window
        """
        self.font = self.font()
        self.title = QLabel("HAND AI")
        self.font.setPointSize(36)
        self.font.setBold(0)
        self.title.setFont(self.font)
        self.mainLayout.addWidget(
            self.title, 0, 10, 2, 2, Qt.AlignmentFlag.AlignCenter)

    def initMenubar(self):
        """
        Initialize the menubar of the window
        """
        # Quit Action (File)
        self.exitAct = QAction('&Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.triggered.connect(QApplication.quit)

        # Train Model Action (File)
        self.trainModelAct = QAction('&Train Model', self)
        self.trainModelAct.triggered.connect(self.train)

        # Download model (File)
        downloadAct = QAction('&Download Dataset', self)
        downloadAct.triggered.connect(self.download)

        # Import train model (File)
        importTrainAct = QAction('&Import Training Dataset', self)
        importTrainAct.triggered.connect(lambda: self.importDataset())

        # Import test model (File)
        importTestAct = QAction('&Import Testing Dataset', self)
        importTestAct.triggered.connect(lambda: self.importDataset(False))
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
        fileMenu.addAction(downloadAct)
        fileMenu.addAction(importTrainAct)
        fileMenu.addAction(importTestAct)
        fileMenu.addAction(self.exitAct)
        # View section
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(trainImagesAct)
        viewMenu.addAction(testImagesAct)

    def initButton(self):
        """
        Initialize the Take Photo Button of the window
        """
        self.takePhotoBtn = QPushButton('Take photo')
        self.mainLayout.addWidget(
            self.takePhotoBtn, 2, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.takePhotoBtn.clicked.connect(self.camera.takePhoto)
        if (self.camera.availableCameras):
            self.camera.captureSession.imageCapture(
            ).imageCaptured.connect(self.camera.handleCapture)

    def initModelSelector(self):
        """
        Initialize the Model Selector of the window
        """
        self.modelsBox = QComboBox(self)
        self.modelsBox.addItems(self.models)
        self.mainLayout.addWidget(
            self.modelsBox, 3, 10, 1, 2, Qt.AlignmentFlag.AlignTop)
        self.modelsBox.currentTextChanged.connect(self.updateModelInfo)

    def initInfo(self):
        """
        Initialize the model info of the window
        """
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

    def initProbabilities(self):
        """
        Initialize the probabilities section of the window
        """
        label = QLabel('Letter Probabilties:')
        self.probabilities = QTextBrowser()
        self.probabilities.setText(
            "A:\nB:\nC:\nD:\nE:\nF:\nG:\nH:\nI:\nJ:\nK:\nL:\nM:\nN:\nO:\nP:\nQ:\nR:\nS:\nT:\nU:\nV:\nW:\nX:\nY:\nZ:")
        self.probabilities.append("\n\n<H1>Result:</H1>")
        self.mainLayout.addWidget(
            label, 5, 10, 1, 2, Qt.AlignmentFlag.AlignBottom)
        self.mainLayout.addWidget(self.probabilities, 6, 10, 16, 2)

    def initCamera(self):
        """
        Initialize the camera of the window
        """
        self.camera = Camera(self)
        self.mainLayout.addWidget(self.camera, 0, 0, 22, 10)

    def updateModelInfo(self, name):
        """
        Update the model infor on change event of the model selector
        """
        if not name:
            return
        self.modelLabel.setText(f"Model: {self.models[name]['model']}")
        self.epochLabel.setText(f"Epoch: {self.models[name]['epoch']}")
        self.batchLabel.setText(f"Batch: {self.models[name]['batchSize']}")
        self.splitLabel.setText(f"Split: {self.models[name]['split']}%")

    def getModel(self):
        """
        Fetch the value from the combo button
        """
        return self.modelsBox.currentText()

    def messageDialog(self, title, message):
        """
        Generate a message dialog box with the given title and message
        """
        MessageDialog(self, title, message)

    def train(self):
        """
        If a dataset is available, open the train config dialog
        """
        if self.checkDataset():
            TrainConfig(self)

    def showTrainImages(self):
        """
        If a dataset is available, open the train images dialog
        """
        if self.checkDataset():
            ImagesDialog(self)

    def showTestImages(self):
        """
        If a dataset is available, open the test images dialog
        """
        if self.checkDataset():
            ImagesDialog(self, True)

    def updatePercentages(self, results, prediction):
        """
        On the results of the prediction, update the percentages
        """
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
        """
        On startup, load the models from the models.sav file
        """
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
        """
        Update the models dictionary with the new model
        """
        self.models[name] = {
            "model": model, "epoch": epoch, "batchSize": batchSize, "split": split}

    def saveModel(self, name, model, epoch, batchSize, split):
        """
        Save the new/updated models dictionary to models.sav file
        """
        self.updateModel(name, model, epoch, batchSize, split)
        self.modelsBox.removeItem(self.modelsBox.findText(name))
        self.modelsBox.addItem(name)
        f = open("./output/models.sav", 'w')
        for key, value in self.models.items():
            f.write(
                f"{key},{value['model']},{value['epoch']},{value['batchSize']},{value['split']}\n")
        f.close()

    def loadModel(self):
        """
        Load a model into the network from the models dictionary
        """
        name = self.getModel()
        model = self.models[name]["model"]
        self.test.load_model(name, model)

    def download(self):
        """
        Creates a thread that downloads the dataset from kaggle without blocking the UI
        """
        worker = Worker(self.downloadDataset)
        self.threadpool.start(worker)
        worker.signals.finished.connect(self.downloadComplete)
        worker.signals.error.connect(lambda: self.messageDialog(
            "Error!", "Failed to download dataset! Make sure you have your kaggle.json setup in your \".kaggle\" folder."))

    def downloadDataset(self):
        """
        Downloads the dataset from kaggle
        """
        import kaggle
        kaggle.api.dataset_download_files(
            'datamunge/sign-language-mnist', path='./data', unzip=True)

    def downloadComplete(self):
        """
        On download complete load the dataset from kaggle and inform the user.
        """
        self.data.loadDatasets()
        self.messageDialog(
            "Success!", "Dataset downloaded successfully!")

    def checkDataset(self):
        """
        Check if a dataset is available
        if not, show an error message
        returns True if dataset is available
        """
        if self.data.test_dataset and self.data.train_dataset:
            return True

        self.messageDialog(
            "Error!", "No Datasets found! Please load a test and train dataset.")
        return False

    def importDataset(self, train: bool = True):
        """
        Imports a single dataset from the clients desktop
        train - whether the dataset will be imported as a training dataset or not.
        """
        self.dialog = QFileDialog()
        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.dialog.setNameFilter("CSV (*.csv)")

        if self.dialog.exec():
            self.data.loadDataset(self.dialog.selectedFiles()[0], train)
