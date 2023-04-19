# Therefore the initial window should have buttons to import data or view the dataset
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QSlider, QComboBox
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

from gui.trainDialog import TrainDialog
from gui.trainWorker import TrainWorker
from neuralnet.train import Train


class TrainConfig(QDialog):
    def __init__(self, parent=None):
        """
        Initializes the training configuration dialog.
        """
        super().__init__(parent=parent)
        self.setWindowTitle("Train a Model")
        self.setFixedSize(350, 190)
        self.initBatchSize()
        self.initEpochs()
        self.initSlider()
        self.initModelSelector()
        self.initName()
        self.initButtons()
        self.show()

    def initBatchSize(self):
        """
        Initializes the batch size input.
        """
        self.batch_size_label = QLabel('Batch Size:', self)
        self.batch_size_label.move(5, 5)
        self.batch_size_line = QLineEdit('4', self)
        self.batch_size_line.setValidator(QIntValidator(1, 9999))
        self.batch_size_line.move(80, 5)
        self.batch_size_line.resize(250, 20)

    def initEpochs(self):
        """
        Initializes the epochs input.
        """
        self.epoch_label = QLabel('Epoch:', self)
        self.epoch_label.move(5, 35)
        self.epoch_line = QLineEdit('5', self)
        self.epoch_line.setValidator(QIntValidator(1, 9999))
        self.epoch_line.move(80, 35)
        self.epoch_line.resize(250, 20)

    def initSlider(self):
        """
        Initializes the slider for the training split.
        """
        self.slider_label = QLabel(
            'Training Split: 100%', self)
        self.slider_label.move(5, 65)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.move(10, 80)
        self.slider.resize(325, 20)
        self.slider.setSingleStep(1)
        self.slider.setRange(1, 100)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(
            lambda value: self.slider_label.setText(f"Training Split: {value}%"))

    def initModelSelector(self):
        """
        Initializes the model selector input.
        """
        itemsList = ["LeNet", "AlexNet", "ResNet"]
        self.model_label = QLabel('Model:', self)
        self.model_label.move(5, 100)
        self.models = QComboBox(self)
        self.models.addItems(itemsList)
        self.models.resize(250, 20)
        self.models.move(80, 100)

    def getModel(self):
        """
        Returns the model selected in the model selector.
        """
        return self.models.currentText()

    def initName(self):
        """
        Initializes the name input.
        """
        self.name_label = QLabel('Name:', self)
        self.name_label.move(5, 130)
        self.name_line = QLineEdit(f'{self.models.currentText()}', self)
        self.models.currentTextChanged.connect(
            lambda value: self.name_line.setText(f"{value}"))
        self.name_line.move(80, 130)
        self.name_line.resize(250, 20)

    def initButtons(self):
        """
        Initializes the train and cancel buttons.
        """
        # Train Button
        self.train_btn = QPushButton('Train', self)
        self.train_btn.resize(95, 20)
        self.train_btn.move(100, 160)
        self.train_btn.clicked.connect(self.train)

        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 160)
        self.cancel_btn.clicked.connect(self.close)

    def train(self):
        """
        Starts the training process on the seperate thread and creates a new training dialog which shows training progress.
        """
        win = self.parent()
        train = Train(win.saveModel)
        dlg = TrainDialog(win)
        worker = TrainWorker(train, self.getModel(), int(
            self.epoch_line.text()), int(self.batch_size_line.text()), self.slider.value(), self.name_line.text())
        worker.signals.progress.connect(dlg.pbar.setValue)
        worker.signals.message.connect(
            dlg.textBrowserTrain.append)
        worker.signals.timer.connect(dlg.setTime)
        worker.signals.finished.connect(
            lambda: dlg.cancel_btn.setText("Finish"))
        dlg.setCancelFunc(train.cancel)
        win.threadpool.start(worker)
        self.close()
