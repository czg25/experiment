import pandas as pd
import numpy as np
import os
from prediction import *
# 获取所有需要遍历的车辆
from areas.statistics_all_car import all_csv_file
from prediction.trans_state_matrix import start_matrix, emission_matrix, transition_matrix

"""
    训练所有文件并保存
"""

# 矩阵保存的文件地址
start_save_path = r"D:\experiment\matrix_20_1000\start"
emission_save_path = r"D:\experiment\matrix_20_1000\emission"
transition_save_path = r"D:\experiment\matrix_20_1000\transition"


def all_start_matrix():
    """
        遍历所有车辆，获取其初始状态转移矩阵
    :return:
    """
    csv_files = all_csv_file()
    for csv_name in csv_files:
        sm = start_matrix(csv_name)
        # em = emission_matrix(csv_name)
        # tm = transition_matrix(csv_name)
        # 都不为空进行保存
        # if sm is not None and em is not None and tm is not None:
        if sm is not None:
            save_matrix(sm, csv_name, start_save_path)
            # save_matrix(em, csv_name, emission_save_path)
            # save_matrix(tm, csv_name, transition_save_path)
        print(csv_name + ":完成保存")


def all_emission_matrix():
    """
        遍历所有车辆，获取发射矩阵
    :return:
    """
    csv_files = all_csv_file()
    for csv_name in csv_files:
        # sm = start_matrix(csv_name)
        em = emission_matrix(csv_name)
        # tm = transition_matrix(csv_name)
        # 都不为空进行保存
        # if sm is not None and em is not None and tm is not None:
        if em is not None:
            # save_matrix(sm, csv_name, start_save_path)
            save_matrix(em, csv_name, emission_save_path)
            # save_matrix(tm, csv_name, transition_save_path)
        print(csv_name + ":完成保存")


def all_translation_matrix():
    """
        遍历所有车辆，获取其初始状态转移矩阵
    :return:
    """
    csv_files = all_csv_file()
    for csv_name in csv_files:
        # sm = start_matrix(csv_name)
        # em = emission_matrix(csv_name)
        tm = transition_matrix(csv_name)
        # 都不为空进行保存
        # if sm is not None and em is not None and tm is not None:
        if tm is not None:
            # save_matrix(sm, csv_name, start_save_path)
            # save_matrix(em, csv_name, emission_save_path)
            save_matrix(tm, csv_name, transition_save_path)
        print(csv_name + ":完成保存")


def save_matrix(data, name, path):
    """
     保存矩阵数据
    :param path: 保存的路径
    :param name:保存的名字
    :param data: 保存的数据
    :return: none
    """
    path = os.path.join(path, name)
    # 一维的需要转置
    # pd.DataFrame(data).T.to_csv(path, index=False, header=False)
    pd.DataFrame(data).to_csv(path, index=False, header=False)


def read_matrix(path) -> np:
    """
        根据需要读取保存的矩阵
    :param path: 读取路径
    :return: 返回一个np数据
    """

    data = pd.read_csv(path, header=None, float_precision="round_trip")
    return np.array(data)


def revise_data():
    """
        转置数据，训练保存的造成的转置，工具函数
    :return:
    """
    # path = r"D:\experiment\matrix_20_5000\emission"

    path = r"D:\experiment\matrix_20_5000\transition"
    csvs = os.listdir(path)

    for csv in csvs:
        path_read_save = os.path.join(path, csv)
        data = read_matrix(path_read_save).T
        pd.DataFrame(data).to_csv(path_read_save, index=False, header=False)
        print(csv, "完成")


def row_sum_test():
    """
        工具类，测试矩阵是否行和为1
    :return:
    """
    path = r"D:\experiment\matrix_20_5000\transition"
    # path = r"D:\experiment\matrix_20_5000\emission"
    lists = os.listdir(path)
    for li in lists[0:10]:
        data = read_matrix(os.path.join(path, li))
        sum_list = data.sum(axis=1)
        print(sum_list)


def save_end_append(csv_path, data):
    """
        在csv文件追加数据，如果csv文件不存在，则创建
    :param csv_path: csv文件路径
    :param data: 保存的数据，一维变量
    :return:
    """
    if not os.path.exists(csv_path):
        pd.DataFrame(columns=["csv_name", "sum_count", "true_count", "precision_rate"]).to_csv(csv_path,
                                                                                               index=False)
    pd_save_data = pd.DataFrame(np.array([data]))
    pd_save_data.to_csv(csv_path, index=False, header=False, mode="a")


if __name__ == '__main__':
    # all_start_matrix()
    # all_emission_matrix()
    # revise_data()
    all_translation_matrix()
    # row_sum_test()
    # save_end_append(r"D:\experiment\result\obs_result\5000_20.csv", [213.2131, 131.12312, 5.2123123, 6.3424])

