import pandas as pd
import os
from areas import compute_areas as ca
from areas import prams_process as prams
import numpy as np
from myCLIQUE import clique_me as my_clique
from dataprocessing import time_slice_extraction as tse

np.set_printoptions(threshold=np.inf)

"""
    实现统计所有car的次数
"""


def init_cell(cut_factor):
    """
        初始化网格
    :return:
    """
    origin = prams.get_origin()
    l_w = prams.get_length_width(prams.range_shanghai())
    test_ca = ca.Areas(origin, cut_factor, l_w)
    cell_lo_count = test_ca.get_cell_count()[0]
    cell_la_count = test_ca.get_cell_count()[1]
    cell = np.zeros(cell_lo_count * cell_la_count, dtype=np.int)
    return cell


def create_areas_instance(cut_factor):
    """
        获取区域划分的实例
    :param cut_factor:  分割因子
    :return:
    """
    origin = prams.get_origin()
    l_w = prams.get_length_width(prams.range_shanghai())
    new_instance = ca.Areas(origin, cut_factor, l_w)
    return new_instance


def single_car(path, cut_factor):
    temp_cell = init_cell(cut_factor)
    # 分割区域的实例
    cc = create_areas_instance(cut_factor)
    # 最大区域长度
    len_temp_cell = len(temp_cell)
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[2, 3])
    for lo, la in zip(csv_data['lon'], csv_data['lat']):
        num = cc.divide_area(lo, la)
        # 判断条件：大于区域长度或者返回-1 都是超过了区域长度，如果temp_cell对应位置为1表示已经访问过
        if num < len_temp_cell and num != -1 and temp_cell[num - 1] != 1:
            temp_cell[num - 1] = 1

    return temp_cell


def find_not_visited(single_cell, temp_cell):
    """
        寻找没有被访问过的区域
    :param single_cell: 所有文件的访问数组
    :param temp_cell:  单个文件的访问数组 一维
    :return: single_cell
    """
    for i in range(len(single_cell)):
        if temp_cell[i] == 1 and single_cell[i] != 1:
            single_cell[i] = temp_cell[i]
    return single_cell


def all_car(cut_factor):
    """
        遍历所有文件
    :param cut_factor:
    :return:
    """
    # 每cur_factor分成一格，向上取整

    # 初始化网格 一维 [0...0]
    cell_ = init_cell(cut_factor)
    files = all_csv_file()
    path = r"D:\experiment\some"
    # 限制遍历的天数
    limit_day = 20

    for csv_file in files:
        single_cell = init_cell(cut_factor)
        for day in os.listdir(path)[0:limit_day]:
            file_path = os.path.join(path, day, csv_file)
            if os.path.exists(file_path):
                temp_cell = single_car(file_path, cut_factor)
                single_cell = find_not_visited(single_cell, temp_cell)
                # print("处理完第" + day + "天" + ": " + csv_file)
            else:
                print("第" + day + "天" + ": " + csv_file + "不存在")
        cell_ += single_cell

    save_result(cell_, cut_factor)


def test_one_car(cut_factor):
    path = r"C:\Users\czg\Desktop\10373_part.csv"
    temp_cell = single_car(path, cut_factor)

    save_result(temp_cell, cut_factor)


def all_csv_file():
    """
        获取所有训练集的名称
    :return:  返回一个列表
    """
    path = r"D:\experiment\some\1"
    file_list = os.listdir(path)
    return file_list


def save_result(data, cur_factor):
    """
        保存数据
        为了便于查看，保持和地图坐标系一样的效果，保存的数据进行了上下翻转；
        读出数据，第一个区域在左上角
        保存数据，第一个区域数据在右下角

    :param cur_factor: 分割因子
    :param data: np_array
    :return:
    """
    # 分割区域的实例
    cc = create_areas_instance(cur_factor)
    # 获取网格横纵格子数
    lo_la = cc.get_cell_count()
    # data1 = np.zeros((13, 12))

    save_path = os.path.join(r"D:\experiment\result", "res_" + str(cur_factor) + ".csv")
    # 一维转换为二维并且上下反转矩阵，显示如地图一样
    # 保存的时候注意reshape 横轴（la）和竖轴（lo）
    data = res_flip(data.reshape((lo_la[1], lo_la[0])))
    df = pd.DataFrame(data, index=None)
    print(df.shape)  # (122, 132)
    df.to_csv(save_path, index=False, header=False)


def path_listdir(path):
    """
    获取路径下的所有文件名
    :param path:
    :return: 列表
    """
    return tse.path_listdir(path)


def res_flip(data):
    """
        传入的二维数组进行上下反转
    :param data:
    :return:
    """
    return np.flipud(data)


def test(cut_factor: int):
    """
        测试某些功能
    :return:
    """
    # ccc = create_areas_instance(cur_factor)
    # print(ccc.get_cell_count())
    # n = ccc.divide_area(121.329066, 31.197058)
    # print(n)
    # a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9],[0,-1,-2]])
    # res_flip(a)
    # ***********************************
    # a = np.zeros(13 * 14)
    # a[82] = 1
    # a = a.reshape((13, 14))
    # print(a)
    # ***********************************
    # test_one_car(cut_factor)
    # ***********************************
    # save_path = os.path.join(r"D:\experiment\result", "res_" + str(cur_factor) + ".csv")
    # print(save_path)
    # ***********************************
    pass


if __name__ == '__main__':
    # cf = [1000, 2000, 3000, 5000]
    cf = [10000]
    for c in cf:
        print("cut_factor=" + str(c) + "运行中。。。")
        all_car(c)
        print("cut_factor=" + str(c) + "运行完成。。。")
        print("******************************************")
    #
    # test()
