import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_d():
    path = r"D:\experiment\result\obs_result\1000_30.csv"
    data = pd.read_csv(path, float_precision="round_trip")
    y = check_data(np.array(data['precision_rate']).flatten())
    x = [i for i in range(len(y))]
    avage = round(sum(y) / len(y), 4)

    # plt.legend(handles=[ln1], labels=[].append(avage))
    # plt.scatter(x, y, marker=".", s=50)
    plt.plot(x, y, color='red', linewidth=0.5, linestyle='-', label='avg:' + str(avage))
    plt.legend()
    plt.show()


def check_data(data):
    lists = []
    for d in list(data)[0:500]:
        if d > 0.9:
            lists.append(d)
    return np.array(lists)


if __name__ == '__main__':
    get_d()
