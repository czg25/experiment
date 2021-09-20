import pandas as pd
from matplotlib import colors
import matplotlib as mpl
import matplotlib.pyplot as plt
from areas import compute_areas as ca
from areas import prams_process as prams
import numpy as np
from myCLIQUE import clique_me as my_clique

"""
去除不需要的区域
"""


# class RemoveArea:
#     def __init__(self, data, threshold):
#         """
#             去除不需要下次遍历的数据
#         :param data: 原始数据
#         :param threshold: 需要移除的区域最小值
#         """
#         self.__data = data
#         self.__threshold = threshold
#
#     def remove(self, area_list):
#         """
#             区域清零
#         :return:
#         """
#         for area in area_list:
#             # loc 为网格中的区域索引
#             loc = my_clique.location_decoding(area)
#             self.__data[loc[0], loc[1]] = 0
#
#     @property
#     def data(self):
#         return self.__data
