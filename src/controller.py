from torch import FloatTensor, max
from PyQt6.QtGui import QImage
from PIL import Image, ImageFilter
import numpy as np
from PyQt6.QtWidgets import QMessageBox, QInputDialog
import time
import threading
from gui.trainThread import TrainThread

from neuralnet.network import Network
from gui.window import Window


class Controller:
    def __init__(self):
        self._network = Network()
        self._window = Window()
        self._initButtons()
        self._initMenuBar()

    def _initButtons(self):
        self._window.takePhotoBtn.clicked.connect(self._takePhoto)
        if (self._window.camera.availableCameras):
            self._window.camera.captureSession.imageCapture(
            ).imageCaptured.connect(self._handleCapture)

    def _initMenuBar(self):

        self._window.trainModelAct.triggered.connect(
            self._trainModel)

        self._window.fileMenu.addAction(self._window.trainModelAct)
        self._window.fileMenu.addAction(self._window.exitAct)

    def _trainModel(self):
        self.traindlg = self._window.trainDialog()
        self.thread = TrainThread(self._network, str(
            self._window.getComboButtonValue()), self.traindlg.pbar)
        self.traindlg.setThread(self.thread)
        self.traindlg.pbar.setValue(0)
        self.thread.start()

    def _takePhoto(self):
        try:
            self._window.camera.captureSession.imageCapture().capture()
        except AttributeError:
            print("No Camera")

    def _handleCapture(self, id: int, capture: QImage):
        image = capture.convertToFormat(QImage.Format.Format_RGB32)
        height = image.height()
        width = image.width()
        pointer = image.constBits()
        pointer.setsize(height * width * 4)
        arr = np.frombuffer(pointer, np.uint8).reshape((height, width, 4))
        preparedImage = self.prepareImage(Image.fromarray(arr[..., 2::-1]))
        print(self.PredictImage(preparedImage))

    def prepareImage(self, image):
        # Converting image to MNIST dataset format

        im = image.convert('L')
        width = float(im.size[0])
        height = float(im.size[1])
        # creates white canvas of 28x28 pixels
        new_image = Image.new('L', (28, 28), (255))

        if width > height:  # check which dimension is bigger
            # Width is bigger. Width becomes 20 pixels.
            # resize height according to ratio width
            nheight = int(round((28.0 / width * height), 0))
            if (nheight == 0):  # rare case but minimum is 1 pixel
                nheight = 1
                # resize and sharpen
            img = im.resize((28, nheight), Image.ANTIALIAS).filter(
                ImageFilter.SHARPEN)
            # calculate horizontal position
            wtop = int(round(((28 - nheight) / 2), 0))
            # paste resized image on white canvas
            new_image.paste(img, (0, wtop))
        else:
            # Height is bigger. Heigth becomes 20 pixels.
            # resize width according to ratio height
            nwidth = int(round((28.0 / height * width), 0))
            if (nwidth == 0):  # rare case but minimum is 1 pixel
                nwidth = 1
                # resize and sharpen
            img = im.resize((nwidth, 28), Image.ANTIALIAS).filter(
                ImageFilter.SHARPEN)
            # caculate vertical pozition
            wleft = int(round(((28 - nwidth) / 2), 0))
            # paste resized image on white canvas
            new_image.paste(img, (wleft, 0))

        pixels = list(new_image.getdata())  # get pixel values
        pixels_normalized = [x / 255.0 for x in pixels]

        return FloatTensor(pixels_normalized).view(1, 28, 28)

    def PredictImage(self, image):
        # self._network.load_model()
        #
        try:
            # Load model takes name as an input, set this to be the value from the combobox
            self._network.load_model(self._window.getComboButtonValue())
            result = self._network.test(image)
            _, prediction = max(result, 1)
            return chr(prediction + ord('A'))
        except:
            print("Model Load Failure!")
            # Open the dialog
            self._window.errorMessageDlg()

        return "Error"
