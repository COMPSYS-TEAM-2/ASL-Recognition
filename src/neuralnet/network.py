import os
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from PyQt6.QtCore import pyqtSignal

from neuralnet.mnist import MNIST
from neuralnet.models.AlexNet import AlexNet
from neuralnet.models.LeNet import LeNet
from neuralnet.models.ResNet import ResNet


class Network():
    EPOCH = 5
    TRAIN_BATCH_SIZE = 4

    def __init__(self):
        # Initialises a new Network instance which loads asl data
        self.train_df_mnist = pd.read_csv("./data/sign_mnist_train.csv")
        self.test_df_mnist = pd.read_csv("./data/sign_mnist_test.csv")
        self.trainloader = DataLoader(
            MNIST(self.train_df_mnist), batch_size=self.TRAIN_BATCH_SIZE, shuffle=True)
        self.testloader = DataLoader(
            MNIST(self.test_df_mnist), batch_size=1, shuffle=True)
        self.switchModel("LeNet")

    def train(self, model, pbar: pyqtSignal, message: pyqtSignal):
        self.switchModel(model)
        message.emit(f"Training {model}...\n")
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)
        self.stop = False
        for epoch in range(self.EPOCH):
            running_loss = 0.0
            for i, data in enumerate(self.trainloader):

                if self.stop == True:
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
                    # Call to the progressbar to update it's progress
                    message.emit('Epoch: %d, Image: %5d, loss: %.3f' %
                                 (epoch + 1, (i + 1) * self.TRAIN_BATCH_SIZE,
                                  running_loss / 800)
                                 )
                    running_loss = 0.0
                if i % 300 == 0:
                    length = len(self.trainloader)
                    pbar.emit((i + epoch * length) /
                              (length * self.EPOCH) * 100)
        pbar.emit(99)
        # message.emit("\nTesting model...")
        message.emit(self.test_all(True))
        self.save_model(model)
        message.emit("\nModel trained and saved")
        pbar.emit(100)

    def test_all(self, train=False):
        # Tests the current model with the test data by default. If train is set to true then will test the model with the training data
        loader = self.testloader
        if (train):
            loader = self.trainloader

        correct = 0
        total = 0
        with torch.no_grad():
            for data in loader:
                images, labels = data
                outputs = self.test(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                # TODO limit number of decimal points
            return f"Accuracy of the network on {'train' if(train) else 'test'} images: {correct/total * 100} %"

    def test(self, image):
        return self.model(image)

    def save_model(self, model):
        # Saves the model under the given name
        # Default name is "model"
        try:
            os.mkdir("./output")
        except:
            pass
        try:
            os.mkdir("./output/models")
        except:
            pass
        torch.save(self.model.state_dict(), f"output/models/{model}.pth")

    def load_model(self, model):
        # Loads the model under the given name.
        # If there are errors it will train the model
        # Default name is "model"
        self.switchModel(model)
        self.model.load_state_dict(
            torch.load(f"output/models/{model}.pth"))

    def switchModel(self, name: str):
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
        self.stop = True
