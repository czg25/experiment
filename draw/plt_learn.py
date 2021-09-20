import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def learn01():
    # 数据点
    x = np.linspace(-100, 100, 50)
    # 显示函数
    y = x ** 2
    # 作图
    plt.plot(x, y)
    plt.show()


def learn02():
    """
    多张figure
    :return:
    """
    x = np.linspace(-100, 100, 50)
    y = x * 2 + 1
    y1 = x ** 2

    plt.figure(num=1)
    plt.plot(x, y)

    plt.figure(num=2, figsize=(5, 5))
    # 画两根线
    plt.plot(x, y1)
    plt.plot(x, y, color="red", linewidth=1.0, linestyle='--')  # 设置图中第二条线的颜色宽度和样式

    plt.show()


def learn03():
    x = np.linspace(-100, 100, 50)
    y = x * 2 + 1
    y1 = x ** 2

    plt.figure(num=2, figsize=(5, 5))
    plt.plot(x, y1)
    plt.plot(x, y, color="red", linewidth=1.0, linestyle='--')

    # 设置横纵坐标的取值范围
    plt.xlim((-100, 100))
    plt.ylim((-100, 100))
    plt.xlabel("xxxxx")
    plt.ylabel("yyyyy")

    # 自定义x y 的坐标
    plt.xticks([0, 10, 20, 30, 40, 50, 60, 70])
    # 可以用字符串来代替坐标的数字，特殊符号用转义符
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70], ["c", "b", "o", "y", "r", "a", "d", "q"])
    plt.show()


def learn04():
    x = np.array([1, 2, 3])
    y = np.array([4,5,6])
    plt.bar(x, y)
    plt.show()


if __name__ == '__main__':
    learn04()
