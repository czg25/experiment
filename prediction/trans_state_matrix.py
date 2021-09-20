import numpy as np
import pandas as pd
import os
import math

from areas import prams_process as prams
from prediction import *
from prediction.data_preparation import path_listdir
from areas import statistics_all_car as sac

"""
    该类训练一个文件
"""

# 划分参数，全局变量
divide_prams = 1000
root_path = r"D:\experiment"


def getMatrixLenWid():
    """
        获取区域网格长宽，注意横向的lon表示列，纵向的lat表示行
        一般是观测状态
    :return:
    """
    length_width = prams.get_length_width(prams.range_shanghai())
    row = math.ceil(length_width[1] / divide_prams)
    col = math.ceil(length_width[0] / divide_prams)
    return row, col


def get_cluster_state():
    """
        获取聚类数据,返回一维数据
    :return:
    """
    path = r"D:\experiment\result\new_some_cluster"
    filename = "res_" + str(divide_prams) + ".csv"
    cells = pd.read_csv(os.path.join(path, filename), header=None)
    # 读取聚类矩阵需要进行翻转
    return np.flipud(np.array(cells)).flatten()


def find_in_clusters(clusters: np, area: int) -> int:
    """
        获取当前区域所在的簇编号
    :param clusters: 聚类数据
    :param area: 给定的编号
    :return: 聚类编号
    """
    clusters_num = clusters[area]
    return int(clusters_num)


def start_matrix(csv_name: str):
    """
        训练初始矩阵Π,单个车俩二十天的聚类
    :return: 如果返回了none，说明不存在的文件，或者说错误文件
    """

    # 获取聚类矩阵,已经是一维
    c_matrix = get_cluster_state()
    # 根据聚类矩阵构建一维空的初始矩阵
    max_state_num = max(c_matrix)
    # 初始隐状态的值是聚类的簇的最大数，+1是要保证0是一个无聚类的区域,
    matrix = np.zeros(int(max_state_num) + 1, dtype=np.int)

    # 获取计算划分区域的类实例
    cc = sac.create_areas_instance(divide_prams)
    sub_path = os.path.join(root_path, "some")
    for day in path_listdir(sub_path)[0:days]:
        csv_path = os.path.join(sub_path, day, csv_name)
        # 文件存在才能执行读取操作
        if os.path.exists(csv_path):
            csv_data = pd.read_csv(csv_path, float_precision="round_trip", index_col=False, usecols=[2, 3])
            for lo, la in zip(csv_data['lon'], csv_data['lat']):
                num = cc.divide_area(lo, la)
                # 不在网格内的点不进行判断
                if num != -1 and num <= len(c_matrix):
                    # 统计初始隐状态的数量
                    clusterNum = find_in_clusters(c_matrix, num)
                    matrix[clusterNum] += 1

    matrix_sum_one_row = matrix.sum()
    if matrix_sum_one_row != 0:
        s_matrix = matrix / matrix_sum_one_row
        return s_matrix
    else:
        return None


def emission_matrix(csv_name: str):
    """
        获取观测矩阵（观察状态）
    :return:
    """
    # data prepared
    clusters = get_cluster_state()
    # 获取最大列数
    max_num = max(clusters) + 1
    # 获取观测状态最大行数
    cells_side_length = getMatrixLenWid()
    m_shape_row = (cells_side_length[0] * cells_side_length[1])
    matrix = np.zeros((int(max_num), m_shape_row), dtype=np.int)
    cc = sac.create_areas_instance(divide_prams)
    sub_path = os.path.join(root_path, "some")

    # get data
    for day in path_listdir(sub_path):
        csv_path = os.path.join(sub_path, day, csv_name)
        if os.path.exists(csv_path):
            csv_data = pd.read_csv(csv_path, float_precision="round_trip", index_col=False, usecols=[2, 3])
            for lo, la in zip(csv_data.lon, csv_data.lat):
                emission_area = cc.divide_area(lo, la)
                # 不在边界直接跳过
                if emission_area > len(clusters) or emission_area == -1:
                    continue
                trans_state = find_in_clusters(clusters, emission_area)
                matrix[trans_state][emission_area] += 1

    # 频率计算概率
    matrix = matrix.astype(np.float)
    matrix_row_sum = matrix.sum(axis=1)
    if matrix_row_sum.sum() == 0:
        return None
    else:
        # 整型转换为浮点矩阵
        for i in range(len(matrix_row_sum)):
            if matrix_row_sum[i] == 0:
                continue
            else:
                for j in range(len(matrix[i])):
                    matrix[i][j] /= matrix_row_sum[i]
    return matrix


def transition_matrix(csv_name: str):
    """
        获取状态转移矩阵(隐状态)
    :return: 如果矩阵和为0返回none，否则返回训练完成的矩阵
    """
    # data prepared
    clusters = get_cluster_state()
    # +1 是考虑簇为0的状态做一个保留
    max_num = int(max(clusters)) + 1
    matrix = np.zeros((max_num, max_num), dtype=np.int)
    cc = sac.create_areas_instance(divide_prams)
    sub_path = os.path.join(root_path, "some")

    # data precess
    for day in path_listdir(sub_path)[0:days]:
        # 前一个状态，如果为负数，未记录前一个状态
        pre_state = -1
        csv_path = os.path.join(sub_path, day, csv_name)
        # 路径的判断是防止在某一天车辆文件不存在，如果不存在就跳过
        if os.path.exists(csv_path):
            csv_data = pd.read_csv(csv_path, float_precision="round_trip", index_col=False, usecols=[2, 3])
            for lo, la in zip(csv_data.lon, csv_data.lat):
                cur_area = cc.divide_area(lo, la)
                # 如果计算出的区域超过了边界，则不进行训练，直接跳过
                if cur_area > len(clusters) or cur_area == -1:
                    continue

                # 获取当前网格编号其对应的簇编号（隐状态）
                cur_state = find_in_clusters(clusters, cur_area)
                # 第一个数据作为前一个状态
                if pre_state < 0:
                    pre_state = cur_state
                else:
                    matrix[pre_state][cur_state] += 1
                    pre_state = cur_state

    # 各行求和算概率
    last_matrix = matrix_after_sum(matrix)
    return last_matrix


def matrix_after_sum(matrix):
    """
        计算每行统计后的概率，如果该行的和全为零，则对应当前状态置为1
    :param matrix:
    :return:
    """
    # axis=1 求行和
    matrix = matrix.astype(np.float)
    rowSum = matrix.sum(axis=1)
    # 如果所有行的和再次求和为零，说明数据不存在，返回none
    if sum(rowSum) == 0:
        return None

    for rowIndex in range(len(rowSum)):
        if rowSum[rowIndex] == 0:
            matrix[rowIndex][rowIndex] = 1
        else:
            for i in range(len(matrix[rowIndex])):
                matrix[rowIndex][i] /= rowSum[rowIndex]

    return matrix


def test():
    data1 = read_matrix(r"D:\experiment\matrix_20_3000\start\00002.csv")
    print(data1.shape)
    data2 = read_matrix(r"D:\experiment\matrix_20_3000\emission\00002.csv")
    print(data2.shape)
    data3 = read_matrix(r"D:\experiment\matrix_20_3000\transition\00002.csv")
    print(data3.shape)


def read_matrix(path) -> np:
    """
        根据需要读取保存的矩阵
    :param path: 读取路径
    :return: 返回一个np数据
    """

    data = pd.read_csv(path, header=None, float_precision="round_trip")
    return np.array(data)


if __name__ == '__main__':
    # 注意修改 全局参数
    # print(transition_matrix("10623.csv"))
    # print(start_matrix("00004.csv"))
    # a = emission_matrix("00004.csv")
    # print(a)
    # print(a.shape)
    pass
