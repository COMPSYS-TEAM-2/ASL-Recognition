import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from mnist import MNIST

from net import Net


class Train():
    EPOCH = 5

    def __init__(self):
        train_df = pd.read_csv("./mnist_data/sign_mnist_train.csv")
        test_df = pd.read_csv("./mnist_data/sign_mnist_test.csv")
        self.trainloader = DataLoader(
            MNIST(train_df), batch_size=4, shuffle=True)
        self.testloader = DataLoader(
            MNIST(test_df), batch_size=4, shuffle=True)
        self.net = Net()

    def train(self):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.net.parameters(), lr=0.001, momentum=0.9)

        running_loss_list = []
        for epoch in range(self.EPOCH):
            running_loss = 0.0
            for i, data in enumerate(self.trainloader):
                inputs, labels = data
                optimizer.zero_grad()

                outputs = self.net(inputs)
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

        correct = 0
        total = 0
        with torch.no_grad():
            for data in self.trainloader:
                images, labels = data
                outputs = self.net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print('Accuracy of the network on train images: ', correct/total)

    def test(self):
        correct = 0
        total = 0
        with torch.no_grad():
            for i, data in enumerate(self.testloader, 0):
                images, labels = data
                outputs = self.net(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print('Accuracy of the network on test images: ', correct/total)
