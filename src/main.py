from network import Network
import matplotlib.pyplot as plt


def main():
    network = Network()
    network.load_model()
    network.test_all()


if __name__ == "__main__":
    main()
