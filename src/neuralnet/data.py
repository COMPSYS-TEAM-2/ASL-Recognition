from neuralnet.mnist import MNIST
from torch.utils.data import DataLoader
import pandas as pd


class Data:
    __instance = None

    def __new__(cls):
        """
        Constructs new instance of Data singleton.
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.init()
        return cls.__instance

    def init(self):
        """
        Initialises the singleton instance of Data.
        """
        self.train_dataset = False
        self.test_dataset = False
        self.loadDatasets()

    def loadDatasets(self):
        """
        Loads the default kaggle datasets if they exist
        """
        self.loadDataset("./data/sign_mnist_train.csv")
        self.loadDataset("./data/sign_mnist_test.csv", False)

    # Function to help the user import their own dataset

    def loadDataset(self, dataset: str, train: bool = True):
        """
        Loads the supplied datasets if they exist
        train - whether the dataset will be imported as a training dataset or not.
        """
        try:
            if train:
                self.train_data = pd.read_csv(dataset)
                self.train_df_mnist = MNIST(self.train_data)
                self.train_dataset = True
            else:
                self.test_data = pd.read_csv(dataset)
                self.test_df_mnist = MNIST(self.test_data)
                self.testloader = DataLoader(
                    self.test_df_mnist, batch_size=1, shuffle=True)
                self.test_dataset = True
        except:
            pass
