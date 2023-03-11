from train import Train
import matplotlib.pyplot as plt


def main():
    train = Train()
    train.train()
    train.test()
    plt.show()


if __name__ == "__main__":
    main()
