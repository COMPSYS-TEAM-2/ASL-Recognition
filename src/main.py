from network import Network
import matplotlib.pyplot as plt


def main():
    network = Network()
    network.train()
    network.test()
    plt.show()


if __name__ == "__main__":
    main()
