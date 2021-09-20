import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from hmmlearn import hmm
from areas import statistics_all_car as sac
# from seqlearn import hmm

from prediction.all_trans_save import read_matrix
from prediction.predict_state import Predict

"""
    一个预测测试demo
"""


# def test():
#     states = ["box 1", "box 2", "box3"]
#     n_states = len(states)
#
#     observations = ["red", "white"]
#     n_observations = len(observations)
#
#     start_probability = np.array([0.2, 0.4, 0.4])
#
#     transition_probability = np.array([
#         [0.5, 0.2, 0.3],
#         [0.3, 0.5, 0.2],
#         [0.2, 0.3, 0.5]
#     ])
#
#     emission_probability = np.array([
#         [0.5, 0.5],
#         [0.4, 0.6],
#         [0.7, 0.3]
#     ])
#     seen = np.array([[0, 1, 0, 1, 1]]).T
#
#     print(viterbi_algorithm(start_probability, transition_probability, emission_probability, seen))
#     print(estimation_problem(start_probability, transition_probability, emission_probability, seen))


def get_matrix():
    start_path = r"C:\Users\czg\Desktop\10374\start10374.csv"
    emsi_path = r"C:\Users\czg\Desktop\10374\emsi10374.csv"
    trans_path = r"C:\Users\czg\Desktop\10374\trans10374.csv"
    start_probability = read_matrix(start_path).flatten()
    transition_probability = read_matrix(trans_path)
    emission_probability = read_matrix(emsi_path)
    return start_probability, transition_probability, emission_probability


def get_observation_sequence():
    csv_path = r"C:\Users\czg\Desktop\10374\test\10374_25.csv"
    csv_data = pd.read_csv(csv_path, float_precision="round_trip", index_col=False, usecols=[2, 3])
    # 2700 - 4000
    cc = sac.create_areas_instance(5000)
    index = 0
    areas = []
    ob_seq = []

    for lo, la in zip(csv_data.lon, csv_data.lat):
        if 2700 <= index <= 4000:
            area = cc.divide_area(lo, la)
            ob_seq.append(area)
            if area not in areas:
                areas.append(area)

        index += 1

    pd.DataFrame(ob_seq).to_csv(r"C:\Users\czg\Desktop\10374\obs.csv", index=False, header=False)
    return areas, ob_seq


def predict(begin, end):
    start_probability, transition_probability, emission_probability = get_matrix()
    observation_sequence_1d = np.array(read_matrix(r"C:\Users\czg\Desktop\10374\obs.csv")).flatten()
    obs = np.array([observation_sequence_1d[begin:end]]).T
    show_obs = observation_sequence_1d[begin:end]
    a = []

    for so in show_obs:
        a.append(exchange(so))

    # print("start_probability:", start_probability.shape)
    # print("transition_probability:", transition_probability.shape)
    # print("emission_probability:", emission_probability.shape)
    print(obs)
    # 观测区域
    print(show_obs)
    print("a:", a)
    p = Predict(start_probability, emission_probability, transition_probability, obs)
    print(p.predict_viterbi())
    print("实际位置：", exchange(observation_sequence_1d[end - 1]))
    print("实际位置a：", a[-1])


def exchange(area):
    path = r"D:\experiment\result\new_some_cluster"
    filename = "res_" + str(5000) + ".csv"
    cells = pd.read_csv(os.path.join(path, filename), header=None)
    # 读取聚类矩阵需要进行翻转
    clusters = np.flipud(np.array(cells)).flatten()
    clusters_num = clusters[area]
    return int(clusters_num)


if __name__ == '__main__':
    # get_observation_sequence()
    # test()
    # predict(1000, 1015)
    predict(1000, 1015)
    # predict(360, 440)
    # predict(360, 370)
