from torch.nn import Conv2d, Sequential, Module, BatchNorm2d, ReLU, MaxPool2d, Linear


class LeNet(Module):
    # Scaled down LeNet model
    def __init__(self):
        super(LeNet, self).__init__()
        self.layer1 = Sequential(
            Conv2d(1, 6, kernel_size=5, stride=1, padding=0),
            BatchNorm2d(6),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = Sequential(
            Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
            BatchNorm2d(16),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2))
        self.fc = Linear(256, 120)
        self.relu = ReLU()
        self.fc1 = Linear(120, 84)
        self.relu1 = ReLU()
        self.fc2 = Linear(84, 26)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.relu(out)
        out = self.fc1(out)
        out = self.relu1(out)
        out = self.fc2(out)
        return out
