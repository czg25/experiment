import random
import pandas as pd
import os
from matplotlib import colors
import matplotlib as mpl
import matplotlib.pyplot as plt
from areas import draw_plot
import numpy as np
from myCLIQUE import clique_me as my_clique
import warnings

np.set_printoptions(threshold=np.inf)

"""
    算法运行的主类
"""


def read_csv_result():
    path = r"D:\experiment\result\res_1000.csv"
    data = np.array(pd.read_csv(path, header=None))

    return data


def area_division(data, threshold):
    """
        使用clique算法进行划分
    :return:
    """

    clique = my_clique.CliqueByMe(data, threshold)
    clique.process()
    # res = clique.clusters_to_array()
    clusters = clique.clusters
    # print(clique.clusters_to_array())
    return clusters


def save_data(last_data: np, filename):

    """
        保存聚类数据
    :param last_data:
    :param filename:
    :return:
    """
    savePath = os.path.join(r"D:\experiment\result\new_some_result", filename)
    pd.DataFrame(last_data).to_csv(savePath, index=False, header=False)


def cycle_div():
    """
        使用clique算法 循环分割区域，threshold逐渐增大，由内向外
        在绘制图时，所有没保存到磁盘的数据都是自顶向下的顺序排列
        读取磁盘的数据，需要进行翻转，内存中的数据不需要
        只有聚类数据需要翻转
    :return:
    """
    path1 = r"D:\experiment\result\new_some\res_1000.csv"
    # path1 = r"D:\experiment\result\res_10000.csv"

    # -------data acquire---------
    max_threshold = 1000
    damping_ratio = 0.9
    # 细分程度
    divide_parm = 3
    cur_threshold = max_threshold * damping_ratio
    last_clusters = []
    # 读取数据要进行翻转，保持一致性,数据为一个矩阵
    # csv文件数据顺序符合地图顺序，读取反转符合数据处理顺序
    data = data_flip(np.array(pd.read_csv(path1, header=None)))
    print("数据的维度：", data.shape)
    # print(data)
    # 保存每个簇所在的网格编号

    while cur_threshold >= max_threshold * (1 - damping_ratio):
        # 使用clique划分
        clusters = area_division(data, cur_threshold)
        # last_clusters最终的区域簇聚类，clusters当前参数cur_threshold的聚类结果
        clusters_separate(last_clusters, clusters)
        remove_area(data, clusters)
        # 参数处理
        cur_threshold -= (1 - damping_ratio) * max_threshold

    print("簇长度", len(last_clusters))
    print(last_clusters)
    # 轮询所有不同密度的簇
    last_clusters = subdivide_clusters(last_clusters, divide_parm)
    print("最后划分的簇的个数：", len(last_clusters))
    print(last_clusters)
    last_data = number_area(data, last_clusters)

    # 保存数据需要对数据进行翻转
    save_data(np.flipud(last_data), path1.split("\\")[-1])
    # 画图,数据从底向上画
    draw_plot.draw_map(last_data)


def subdivide_clusters(last_clusters: list, divide_parm: int) -> list:
    """
        clique算法生成的簇，细分并编号
    :param divide_parm:
    :param last_clusters:
    :return:
    """
    new_cluster = []
    # for sub_cluster in last_clusters:
    #     cluster_length = len(sub_cluster)
    #     # 超过3个需要手动划分
    #     if cluster_length > divide_parm:
    #         count = 0
    #         while count < cluster_length:
    #             if cluster_length - count < divide_parm:
    #                 new_cluster.append(sub_cluster[count:])
    #             else:
    #                 new_cluster.append(sub_cluster[count:(count + divide_parm)])
    #             count += divide_parm
    #     else:
    #         new_cluster.append(sub_cluster)
    for sub_cluster in last_clusters:
        cluster_length = len(sub_cluster)
        # 长度超过divide_parm 需要进行再次划分
        if cluster_length > divide_parm:
            divide_subarea(sub_cluster, new_cluster, divide_parm)
        else:
            new_cluster.append(sub_cluster)
    return new_cluster


def replace_void(temp: list, sub_cluster: list):
    """
        sub_cluster 中temp包含的元素置为空
    :param temp:
    :param sub_cluster:
    """
    for i in range(len(sub_cluster)):
        if sub_cluster[i] in temp:
            sub_cluster[i] = ''


def divide_subarea(sub_cluster: list, new_cluster: list, divide_parm: int):
    """
        分割长度过长的簇，保持每个簇的长度不超过divide_parm，同时保证子簇的网格相连（簇长为1的除外）
    :param sub_cluster: 需要分割的簇
    :param new_cluster: 划分的簇要拼接到new_cluster
    :param divide_parm: 分割参数，每次递归需要减小
    :return:
    """
    if divide_parm < 1:
        return
    # sort(key=lambda sc: my_clique.location_decoding(sc)[0],reverse=False)
    # sub_cluster.sort(key=lambda sc: my_clique.location_decoding(sc)[1],reverse=False)
    if divide_parm > 1:
        for s in sub_cluster:
            temp = [s]
            if s == '':  # 如果为空跳过循环
                continue
            s_neighbor = get_neighbor(s)
            for sn in s_neighbor:
                if sn in sub_cluster:
                    temp.append(sn)
                if len(temp) == divide_parm:
                    new_cluster.append(temp.copy())
                    # 如果相邻网格编号出现在列表后几个元素，置为空，不需要在遍历
                    replace_void(temp, sub_cluster)
                    break
    # 如果划分参数为1，则直接进行划分
    elif divide_parm == 1:
        for s_rest_one in sub_cluster:
            new_cluster.append([s_rest_one])
    if len(sub_cluster) > 0:
        sc_next = [sc for sc in sub_cluster if sc != '']

        divide_subarea(sc_next, new_cluster, divide_parm - 1)  # 递归遍历


def get_neighbor(s) -> list:
    """
        返回邻接（上下左右）网格，此方法没有处理越界，但不影响
    :param s: 给定网格坐标，
    :return: 返回四个元素的列表
    """
    s_temp = my_clique.location_decoding(s)
    return [my_clique.location_encoding(s_temp[0] + 1, s_temp[1]),
            my_clique.location_encoding(s_temp[0] - 1, s_temp[1]),
            my_clique.location_encoding(s_temp[0], s_temp[1] + 1),
            my_clique.location_encoding(s_temp[0], s_temp[1] - 1),
            ]


def number_area(data, last_clusters):
    """
        给每个簇编号，方便绘图
    :param data: 原始数据，取二维长度
    :param last_clusters: 划分的簇
    :return: 返回区域已经编号的网格矩阵
    """
    data_zero = np.zeros((len(data), len(data[0])))
    c_index = 0
    for ld in last_clusters:
        c_index += 1
        for c in ld:
            index_cell = my_clique.location_decoding(c)
            data_zero[index_cell[0]][index_cell[1]] = c_index
    return data_zero


def clusters_separate(last_data, clusters):
    """
        每个簇进行分离，赋值到新的数组当中
    :param clusters:
    :param last_data:
    :param clusters:
    :return:
    """
    for c in clusters:
        last_data.append(c)


def remove_area(data, cluster):
    """
        根据cluster中的数据清空data的区域数据，下次处理不需要这些数据
    :param data:
    :param cluster: 簇数据
    :return:
    """
    for c in cluster:
        for i in range(len(c)):
            temp = my_clique.location_decoding(c[i])
            data[temp[0]][temp[1]] = 0


def data_flip(data):
    """
        传入的二维数组进行上下反转
    :param data:
    :return:
    """
    return np.flipud(data)


def test():
    zero = np.zeros((8, 8))
    a = ['4-4', '5-4', '4-5', '6-4', '5-5', '4-6', '6-5', '5-6', '7-5', '6-6', '5-7']
    print(a)
    for a1 in a:
        index = my_clique.location_decoding(a1)
        zero[index[0]][index[1]] = 1
    b = []

    print(zero)
    divide_subarea(a, b, 3)
    print(b)
    print(number_area(zero, b))


if __name__ == '__main__':
    # draw_map()
    cycle_div()
