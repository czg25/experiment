from geopy.distance import great_circle
import math
import os
import numpy as np
import pandas as pd
from dataprocessing import time_slice_extraction as tse

"""
    区域的参数设置以及经纬度距离的计算
"""


def distance(lo, la, lo1, la1):
    """
        计算两个经纬度之间的距离
    :param lo:
    :param la:
    :param lo1:
    :param la1:
    :return: 返回值单位为米
    """
    point1 = (la, lo)
    point2 = (la1, lo1)
    return great_circle(point1, point2).m


def get_origin():
    """
        返回原点坐标
    """
    # 旧数据
    return [120.852326, 30.691701]
    # return [120.800000, 30.491701]


def range_shanghai():
    """
        120.852326~122.118227 30.691701~31.874634
    :return: 返回上海的极值坐标顶点
    """
    max_min = np.array(
        # [[120.852326, 30.691701], [122.118227, 30.691701], [120.852326, 30.691701], [120.852326, 31.874634]],
        [[120.852326, 30.691701], [122.118227, 30.691701], [120.852326, 30.691701], [120.852326, 31.874634]],
        dtype=np.float64)
    return max_min


def get_length_width(max_min):
    length = distance(max_min[0][0], max_min[0][1], max_min[1][0], max_min[1][1])
    width = distance(max_min[2][0], max_min[2][1], max_min[3][0], max_min[3][1])
    return [length, width]


def path_listdir(path: str) -> list:
    """
    获取路径下的所有文件名
    :param path:
    :return: 列表
    """
    return tse.path_listdir(path)


def find_all_file():
    path = r"D:\experiment\some"
    min_lon = 0
    min_lat = 0
    is_first = False
    for sub_p in path_listdir(path)[0:20]:
        csv_files_path = os.path.join(path, sub_p)
        for csv_name in os.listdir(csv_files_path):
            temp = find_min_max(os.path.join(csv_files_path, csv_name))
            if not is_first:
                min_lon = temp[0]
                min_lat = temp[1]
                is_first = True
            else:
                if min_lon < temp[0]:
                    min_lon = temp[0]
                if min_lat < temp[1]:
                    min_lat = temp[1]

    return [min_lon, min_lat]


def find_min_max(path):
    """
        返回每个列的最小值所在的那一行
    :param path:
    :return:
    """
    # path = r"C:\Users\czg\Desktop\10373.csv"
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[2, 3])
    temp = np.array(csv_data)
    return np.min(temp, axis=0)


if __name__ == '__main__':
    print(get_length_width(range_shanghai()))
    # print(find_all_file())
