import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from net import Net


class Train():
    def train(self):
        pass


class MNIST(Dataset):
    def __init__(self, df):
        self.rows = len(df)
        self.imgnp = df.iloc[:self.rows, 1:].values
        self.labels = df.iloc[:self.rows, 0].values

    def __len__(self):
        return self.rows

    def __getitem__(self, idx):
        image = torch.tensor(
            self.imgnp[idx], dtype=torch.float) / 255  # Normalize
        image = image.view(1, 28, 28)  # (channel, height, width)
        label = self.labels[idx]
        return (image, label)


train_df = pd.read_csv(
    "./mnist_data/sign_mnist_train.csv")
test_df = pd.read_csv(
    "./mnist_data/sign_mnist_test.csv")

trainloader = DataLoader(MNIST(train_df), batch_size=4, shuffle=True)
testloader = DataLoader(MNIST(test_df), batch_size=4, shuffle=True)

net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.002, momentum=0.9)

running_loss_list = []
for epoch in range(2):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        optimizer.zero_grad()

        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 200 == 199:
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 200)
                  )
            running_loss_list.append(running_loss)
            running_loss = 0.0
print('Finished Training')
plt.plot(running_loss_list)

correct = 0
total = 0
with torch.no_grad():
    for data in trainloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print('Accuracy of the network on train images: ', correct/total)

correct = 0
total = 0
with torch.no_grad():
    for i, data in enumerate(testloader, 0):
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print('Accuracy of the network on test images: ', correct/total)

plt.show()
