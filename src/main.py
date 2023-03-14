import os
import torch
from image import prepare_image
from network import Network
import matplotlib.pyplot as plt


def main():
    network = Network()
    network.load_model()
    network.test_all()
    image = prepare_image("data/asl/O.png")
    result = network.test(image)
    _, predicted = torch.max(result, 1)
    print(result, chr(predicted + ord('A')))
    plt.imshow(image[0], cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()
