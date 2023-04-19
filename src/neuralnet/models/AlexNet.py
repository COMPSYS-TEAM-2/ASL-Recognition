from torch import Tensor
from torch.nn import Conv2d, Sequential, Module, BatchNorm2d, ReLU, MaxPool2d, Dropout, Linear


class AlexNet(Module):
    # Scaled down AlexNet model for MNIST data
    def __init__(self):
        super(AlexNet, self).__init__()
        self.layer1 = Sequential(
            Conv2d(1, 32, kernel_size=5, stride=1, padding=0),
            BatchNorm2d(32),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = Sequential(
            Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(64),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2))
        self.layer3 = Sequential(
            Conv2d(64, 96, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(96),
            ReLU())
        self.layer4 = Sequential(
            Conv2d(96, 96, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(96),
            ReLU())
        self.layer5 = Sequential(
            Conv2d(96, 64, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(64),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=1))
        self.fc = Sequential(
            Dropout(0.5),
            Linear(1600, 2048),
            ReLU())
        self.fc1 = Sequential(
            Dropout(0.5),
            Linear(2048, 2048),
            ReLU())
        self.fc2 = Sequential(
            Linear(2048, 26))

    def forward(self, x: Tensor):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out
