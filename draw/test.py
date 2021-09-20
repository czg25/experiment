import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def f():
    my_dpi = 126
    # 设置宽高
    fig = plt.figure(figsize=(580 / my_dpi, 480 / my_dpi))

    mpl.rcParams['axes.linewidth'] = 0.5
    mpl.rcParams['xtick.major.size'] = 0.0
    mpl.rcParams['ytick.major.size'] = 0.0
    d = 0.01
    ax = fig.add_axes([d, d, 1 - 2 * d, 1 - 2 * d])
    np.random.seed(3)
    I = np.zeros((8, 8, 4))

    I[:, :] = mpl.colors.to_rgba("C1")
    I[..., 3] = np.random.uniform(0.25, 1.0, (8, 8))
    print(I.shape)
    ax.imshow(I, extent=[0, 8, 0, 8], interpolation="nearest")
    ax.set_xlim(0, 8), ax.set_xticks(np.arange(1, 8))
    ax.set_ylim(0, 8), ax.set_yticks(np.arange(1, 8))
    ax.grid(linewidth=0.25, color="white")
    plt.show()


def colormap():
    # 白粉紫蓝
    cdict = ['#FFFFFF', '#FFB6C1', '#800080', '#0000FF']
    # 按照上面定义的colordict，将数据分成对应的部分，indexed：代表顺序
    return colors.ListedColormap(cdict, 'indexed')


def a():
    data = [[1, 3, 1], [3, 3, 2], [1, 4, 0]]
    # data = [[1, 0, 1], [0, 0, 0], [0, 0, 0]]
    fig = plt.figure(figsize=(2.5, 2.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(data, extent=[0, 3, 0, 3], interpolation="none", origin="lower", vmin=0.99,
              cmap=colormap())  # origin="lower":默认自底向上画
    # ax.grid(linewidth=0.25, color="black")

    plt.show()


if __name__ == '__main__':
   a()
