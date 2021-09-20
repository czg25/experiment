import random
from matplotlib import colors
import matplotlib as mpl
import matplotlib.pyplot as plt
from areas import compute_areas as ca
from areas import prams_process as prams
import numpy as np

from myCLIQUE import clique_me as my_clique


def draw_map(data):
    # data = [[1, 0, 1], [0, 3, 0], [0, 0, 0]]
    length = len(data)
    width = len(data[0])
    # 获取data中的最大值
    max_value = max(map(max, data))
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(data, extent=[0, length, 0, width], interpolation="none", origin="lower", vmin=0.5,
              cmap=colormap(max_value))  # origin="lower":默认自底向上画
    # ax.grid(linewidth=0.25, color="black")

    plt.show()


def random_color():
    """
        生成随机16进制随机颜色代码
    :return:
    """
    colors1 = '0123456789ABCDEF'
    num = "#"
    for i in range(6):
        num += random.choice(colors1)
    return num


def colormap(max_value):
    # cdict = ['#FFFFFF', '#B0E4DA', '#B8860B', '#006400', '#8B008B',
    #          '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1',
    #          '#9400D3', '#FF1493',
    #          '#00BFFF',
    #          '#696969',
    #          '#1E90FF',
    #          '#B22222',
    #          '#FFFAF0',
    #          '#228B22',
    #          'fuchsia', '#FF00FF',
    #          '#DCDCDC',
    #          '#F8F8FF',
    #          '#FFD700',
    #          '#DAA520',
    #          '#808080',
    #          '#008000',
    #          '#ADFF2F',
    #          '#F0FFF0',
    #          '#FF69B4',
    #          '#CD5C5C',
    #          '#4B0082',
    #          '#FFFFF0',
    #          '#F0E68C',
    #          '#E6E6FA',
    #          '#FFF0F5',
    #          '#7CFC00',
    #          '#FFFACD',
    #          '#ADD8E6',
    #          '#F08080',
    #          '#E0FFFF',
    #          '#FAFAD2',
    #          '#90EE90',
    #          '#D3D3D3',
    #          '#FFB6C1',
    #          '#FFA07A',
    #          '#20B2AA',
    #          '#87CEFA',
    #          '#778899',
    #
    #          '#FFFFE0',
    #          '#00FF00',
    #          '#32CD32',
    #          ]
    # cdict = ['#FFFFFF',
    #          '#696969',
    #          '#1E90FF',
    #          '#B22222',
    #          '#FFFAF0',
    #          '#228B22',
    #          'fuchsia', '#FF00FF',
    #          '#DCDCDC',
    #          '#F8F8FF',
    #          '#FFD700',
    #          '#DAA520',
    #          '#808080',
    #          '#008000',
    #          '#ADFF2F']
    # '#F0FFF0',
    # '#FF69B4',
    # '#CD5C5C',
    # '#4B0082',
    # '#FFFFF0',
    # '#F0E68C',
    # '#E6E6FA', ]
    # 按照上面定义的colordict，将数据分成对应的部分，indexed：代表顺序
    cdict = ['#FFFFFF']
    while 0 < max_value:
        color = random_color()
        if color not in cdict:
            max_value -= 1
            cdict.append(color)
        if len(cdict) > 10000:  # 生成的颜色过多，放弃生成
            break

    return colors.ListedColormap(cdict, 'indexed')
