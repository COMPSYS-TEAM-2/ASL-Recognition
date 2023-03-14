import os
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from mnist import MNIST

from model import Model


class Network():
    EPOCH = 5

    def __init__(self):
        # Initialises a new Network instance which loads asl data
        train_df = pd.read_csv("./data/sign_mnist_train.csv")
        test_df = pd.read_csv("./data/sign_mnist_test.csv")
        self.trainloader = DataLoader(
            MNIST(train_df), batch_size=4, shuffle=True)
        self.testloader = DataLoader(
            MNIST(test_df), batch_size=1, shuffle=True)
        self.model = Model()

    def train(self):
        # Trains the current model with the training data
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)

        running_loss_list = []
        for epoch in range(self.EPOCH):
            running_loss = 0.0
            for i, data in enumerate(self.trainloader):
                inputs, labels = data
                optimizer.zero_grad()

                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 800 == 799:
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 800)
                          )
                    running_loss_list.append(running_loss)
                    running_loss = 0.0
        print('Finished Training')
        plt.plot(running_loss_list)
        self.test_all(True)
        self.save_model()

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
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            print(
                f"Accuracy of the network on {'train' if(train) else 'test'} images: ", correct/total)

    def test(self, image):
        return self.model(image)

    def save_model(self, name="model"):
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
        torch.save(self.model.state_dict(), f"output/models/{name}.pth")

    def load_model(self, name="model"):
        # Loads the model under the given name.
        # If there are errors it will train the model
        # Default name is "model"
        try:
            self.model.load_state_dict(
                torch.load(f"output/models/{name}.pth"))
            print("Model Load Success!")
        except:
            print("Model Load Failure!\nTraining Model")
            self.train()
