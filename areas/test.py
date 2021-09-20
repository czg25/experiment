# import pandas as pd
# from areas import compute_areas as ca
# from areas import prams_process as prams
# import numpy as np
# from myCLIQUE import clique_me as my_clique
#
# np.set_printoptions(threshold=np.inf)
#
#
# def init_cell(cut_factor):
#     """
#         初始化网格
#     :return:
#     """
#     origin = prams.get_origin()
#     l_w = prams.get_length_width(prams.range_shanghai())
#     test_ca = ca.Areas(origin, cut_factor, l_w)
#     cell_lo_count = test_ca.get_cell_count()[0]
#     cell_la_count = test_ca.get_cell_count()[1]
#
#     cell = np.zeros(cell_lo_count * cell_la_count, dtype=np.int)
#     return cell
#
#
# def create_areas_instance(cut_factor):
#     """
#         获取区域划分的实例
#     :param cut_factor:  分割因子
#     :return:
#     """
#     origin = prams.get_origin()
#     l_w = prams.get_length_width(prams.range_shanghai())
#     new_instance = ca.Areas(origin, cut_factor, l_w)
#     return new_instance
#
#
# def get_areas():
#     """
#         获取单个文件的在区域中经过的网格统计
#     :return: np.array
#     """
#     cur_factor = 5000
#     # 初始化网格
#     cell_ = init_cell(cur_factor)
#     # 分割区域的实例
#     cc = create_areas_instance(cur_factor)
#     # 获取网格横纵格子数
#     lo_la = cc.get_cell_count()
#     path = r"C:\Users\czg\Desktop\10373.csv"
#     csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[2, 3])
#     for lo, la in zip(csv_data['lon'], csv_data['lat']):
#         # print((lo, la))
#         num = cc.divide_area(lo, la)
#         if num > 0:
#             cell_[num - 1] += 1
#     return cell_.reshape(lo_la[0], lo_la[1])
#
#
# if __name__ == '__main__':
#     data1 = get_areas()
#     s = my_clique.CliqueByMe(data1, 100)
#     s.process()
#     # array_1 = s.clusters_to_array()
#     array_2 = s.clusters
#     print(array_2)
