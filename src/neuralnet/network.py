import os
import time
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from PyQt6.QtCore import pyqtSignal
from torch.utils.data import random_split
from neuralnet.mnist import MNIST
from neuralnet.models.AlexNet import AlexNet
from neuralnet.models.LeNet import LeNet
from neuralnet.models.ResNet import ResNet


class Network():
    def __init__(self):
        """
        Initialises a new Network instance which loads the datasets if they exist.
        """
        self.loadDatasets()

    def setSaveMethod(self, save_method):
        """
        Sets the save method from the window to be used by the network class.
        """
        self.save_method = save_method

    def train(self, model, name, pbar: pyqtSignal, message: pyqtSignal, timer: pyqtSignal, EPOCH=5, BATCH_SIZE=4, SPLIT=100):
        """
        Trains the model with the given parameters, emits the progress to the progressbar, the message to the message box and saves the model.
        """
        message.emit(f"Training {name}...\n")

        self.switchModel(model)

        if (SPLIT != 100):
            # Randomly splits the dataset into a training and testing set with the given split
            train_data, test_data = random_split(
                self.train_df_mnist, [SPLIT/100, 1-SPLIT/100])
        else:
            train_data = self.train_df_mnist

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
        if (SPLIT != 100):
            message.emit(
                f"Accuracy of the network on the remaining train images: {self.test_all(test_data)} %")
        message.emit(
            f"Accuracy of the network on the test images: {self.test_all()} %")

        self.save_model(name, model, EPOCH, BATCH_SIZE, SPLIT)
        message.emit(f"\n{name} trained and saved!")
        pbar.emit(100)

    def test_all(self, dataset=None, percentage=True):
        """
        Tests the current model with the test data by default.
        If a dataset is supplied then it will test the model with the dataset.
        If percentage is True then it will return the percentage of correct predictions.
        If percentage is False then it will return the number of correct predictions and the total number of predictions.
        """
        loader = self.testloader
        if (dataset):
            loader = DataLoader(dataset, batch_size=1, shuffle=True)

        correct = 0
        total = 0
        with torch.no_grad():
            for data in loader:
                images, labels = data
                outputs = self.test(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            if percentage:
                return round(correct/total * 100, 2)
            else:
                return correct, total

    def test(self, image):
        """Tests the current model with the given image"""
        return self.model(image)

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

    def load_model(self, name, model):
        """
        Loads the model under the given name.
        """
        self.switchModel(model)
        self.model.load_state_dict(
            torch.load(f"output/models/{name}.pth"))

    def switchModel(self, name: str):
        """Switches the model to the given name"""
        name = name.lower()
        if name == "lenet":
            self.model = LeNet()
        elif name == "alexnet":
            self.model = AlexNet()
        elif name == "resnet":
            self.model = ResNet()
        else:
            self.model = LeNet()

    def cancel(self):
        """Stops the training process on another thread"""
        self.stop = True

    def loadDatasets(self):
        """Loads the datasets if they exist"""
        try:
            self.train_df_mnist = MNIST(
                pd.read_csv("./data/sign_mnist_train.csv"))
            self.test_df_mnist = MNIST(
                pd.read_csv("./data/sign_mnist_test.csv"))
            self.testloader = DataLoader(
                self.test_df_mnist, batch_size=1, shuffle=True)
            self.dataset = True
        except:
            self.dataset = False
