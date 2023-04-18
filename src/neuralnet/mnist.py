from torch.utils.data import Dataset
import torch


class MNIST(Dataset):
    # A Class to represent the MNIST dataset
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
