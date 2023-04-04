# Therefore the initial window should have buttons to import data or view the dataset
from PyQt6.QtWidgets import QPushButton, QComboBox, QDialog, QProgressBar, QTextBrowser,QMessageBox,QVBoxLayout
from gui.trainingPrgBar import *



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
        self.train_btn.clicked.connect(self.show_popUp)


        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 375)
        self.cancel_btn.clicked.connect(self.close)

   
    
    def showPbar(self):

        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.button = QPushButton('Start', self)
        self.button.move(0, 30)

        self.show()

        self.button.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        count = 0
        while count < 200:
            count += 1
            time.sleep(1)
            self.progress.setValue(count)

    def show_popUp(self):
        self.showPbar()



