import torch
from torch.utils.data import DataLoader

from neuralnet.data import Data
from neuralnet.models.switchModel import switchModel


class Test():
    def __init__(self):
        self.data = Data()

    def test(self, image):
        """Tests the current model with the given image"""
        return self.model(image)

    def test_all(self, dataset=None, percentage=True):
        """
        Tests the current model with the test data by default.
        If a dataset is supplied then it will test the model with the dataset.
        If percentage is True then it will return the percentage of correct predictions.
        If percentage is False then it will return the number of correct predictions and the total number of predictions.
        """
        loader = self.data.testloader
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

    def load_model(self, name, model):
        """
        Loads the model under the given name.
        """
        self.model = switchModel(model)
        self.model.load_state_dict(torch.load(f"output/models/{name}.pth"))

    def importModel(self, model):
        self.model = model
