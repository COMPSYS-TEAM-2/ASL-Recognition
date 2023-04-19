from neuralnet.models.AlexNet import AlexNet
from neuralnet.models.LeNet import LeNet
from neuralnet.models.ResNet import ResNet


def switchModel(name: str):
    """Switches the model to the given name"""
    name = name.lower()
    if name == "lenet":
        return LeNet()
    elif name == "alexnet":
        return AlexNet()
    elif name == "resnet":
        return ResNet()
    else:
        return LeNet()
