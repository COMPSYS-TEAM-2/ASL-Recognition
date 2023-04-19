import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from PyQt6.QtCore import pyqtSignal
from torch.utils.data import random_split

from neuralnet.data import Data
from neuralnet.models.switchModel import switchModel
from neuralnet.test import Test


class Train():
    def __init__(self, save_method):
        """
        Initialises a new Network instance which loads the datasets if they exist.
        """
        self.data = Data()
        self.test = Test()
        self.save_method = save_method

    def train(self, model, name, pbar: pyqtSignal, message: pyqtSignal, timer: pyqtSignal, EPOCH=5, BATCH_SIZE=4, SPLIT=100):
        """
        Trains the model with the given parameters, emits the progress to the progressbar, the message to the message box and saves the model.
        """
        message.emit(f"Training {name}...\n")

        self.model = switchModel(model)

        if (SPLIT != 100):
            # Randomly splits the dataset into a training and testing set with the given split
            train_data, test_data = random_split(
                self.data.train_df_mnist, [SPLIT/100, 1-SPLIT/100])
        else:
            train_data = self.data.train_df_mnist

        trainloader = DataLoader(
            train_data, batch_size=BATCH_SIZE, shuffle=True)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)
        self.stop = False
        start = time.time()

        for epoch in range(EPOCH):
            running_loss = 0.0
            for i, data in enumerate(trainloader):

                if self.stop == True:
                    # Check if the stop flag is true and if so, stop the training
                    raise StopIteration

                inputs, labels = data
                optimizer.zero_grad()

                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 800 == 799:
                    # Call to the message box and display the loss
                    message.emit('Epoch: %d/%d, Image: %5d, loss: %.3f' %
                                 (epoch + 1, EPOCH, (i + 1) * BATCH_SIZE,
                                  running_loss / 800)
                                 )
                    running_loss = 0.0
                if i % 300 == 0 and i != 0:
                    # Call to the progressbar to update it's progress
                    length = len(trainloader)
                    percentage = (i + epoch * length) / (length * EPOCH)
                    pbar.emit(percentage * 100)
                    elapsed = time.time() - start
                    timer.emit(elapsed/percentage-elapsed)

        pbar.emit(99)
        message.emit("\nTesting model...")
        self.test.importModel(self.model)
        if (SPLIT != 100):
            message.emit(
                f"Accuracy of the network on the remaining train images: {self.test.test_all(test_data)} %")
        message.emit(
            f"Accuracy of the network on the test images: {self.test.test_all()} %")

        self.save_model(name, model, EPOCH, BATCH_SIZE, SPLIT)
        message.emit(f"\n{name} trained and saved!")
        pbar.emit(100)

    def save_model(self, name, model, epoch, batch_size, split):
        """
        Saves the model under the given name with the given parameters.
        """
        try:
            os.mkdir("./output")
        except:
            pass
        try:
            os.mkdir("./output/models")
        except:
            pass
        self.save_method(name, model, epoch, batch_size, split)
        torch.save(self.model.state_dict(), f"output/models/{name}.pth")

    def cancel(self):
        """Stops the training process on another thread"""
        self.stop = True
