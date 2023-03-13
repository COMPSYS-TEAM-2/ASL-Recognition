from image import prepare_image
from network import Network
import matplotlib.pyplot as plt


def main():
    network = Network()
    network.load_model()
    network.test_all()
    image = prepare_image("data/asl/O.png")
    print(image)
    plt.imshow(image, cmap='gray')
    plt.show()


if __name__ == "__main__":
    main()
