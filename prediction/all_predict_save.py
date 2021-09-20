import pandas as pd
import numpy as np
import os
from prediction import *
# 获取所有需要遍历的车辆
from areas.statistics_all_car import all_csv_file
from prediction.HHMtest import get_matrix
from prediction.all_trans_save import read_matrix, save_end_append
from prediction.predict_state import Predict
from prediction.trans_state_matrix import start_matrix, emission_matrix, transition_matrix
from areas import statistics_all_car as sac

"""
    预测所有的测试集，并保存
"""

divide_parm = 3000


# def random_predict(csv_name: str) -> int:
#     start, emission, transition = get_all_matrix(csv_name)
#
#     # pre = Predict(start_matrix, emission_matrix, transition_matrix,)
#     return 1
#
#
# def get_all_matrix(csv_name: str):
#     return 1, 2, 3
#
#
# def random_generator(max_num):
#     pass

def check_bounds(data, begin, end, emission_bounds):
    """
        边界检查，超过边界的不进行预测
    :param data: 观测数据
    :param begin: 起始位置
    :param end: 结束位置（不包含）
    :param emission_bounds: 边界最大值
    :return: true 表示没有越界
    """
    for i in range(begin, end):
        if data[i] > emission_bounds:
            return False
    return True


def section(data, seq_length, emission_bounds) -> list:
    """
        根据测试集，划分测试集轨迹，每seq_length为一段；
        [begin,end) 半开区间
    :param emission_bounds: 越界检查参数
    :param data: 测试集
    :param seq_length: 轨迹长度
    :return:  给定测试集data，返回其轨迹分段
    """
    data_length = len(data)
    result_seq = []
    i = 0
    while i <= data_length:
        if i + seq_length > data_length:
            break
        if check_bounds(data, i, i + seq_length, emission_bounds):
            # 在此做一个保留处理，如果没有应该直接判断错误（未做）
            result_seq.append((i, i + seq_length))
        i = i + seq_length
    return result_seq


def get_three_matrix(csv_name):
    """
        根据文件名获取其训练好的三个矩阵
    :param csv_name:
    :return:
    """
    root_path = r"D:\experiment"
    start_path = os.path.join(root_path, "matrix_20_" + str(divide_parm), "start", csv_name)
    emsi_path = os.path.join(root_path, "matrix_20_" + str(divide_parm), "emission", csv_name)
    trans_path = os.path.join(root_path, "matrix_20_" + str(divide_parm), "transition", csv_name)

    start_probability = read_matrix(start_path).flatten()
    emission_probability = read_matrix(emsi_path)
    transition_probability = read_matrix(trans_path)

    return start_probability, emission_probability, transition_probability


def predict_all_cars(seq_length):
    csv_files = all_csv_file()
    # csv_files = ["00028.csv"]  # test
    obs_path = os.path.join(r"D:\experiment\obs", "obs_" + str(divide_parm))
    for csv_name in csv_files:
        sum_count = 0
        true_count = 0
        for test_day in os.listdir(obs_path):
            csv_path = os.path.join(obs_path, test_day, csv_name)
            # 如果路径存在
            if os.path.exists(csv_path):
                # 获取总的预测次数和正确次数
                sc, tc = predict_one_day(csv_path, seq_length)
                # 累加次数
                true_count += tc
                sum_count += sc
        precision_rate = 0
        if sum_count != 0:
            precision_rate = true_count / sum_count
        save_data = [csv_name, sum_count, true_count, precision_rate]

        # 保存数据
        # 根据参数拼接保存路径
        result_save_path = os.path.join(r"D:\experiment\result\obs_result",
                                        str(divide_parm) + "_" + str(seq_length) + ".csv")
        save_end_append(result_save_path, save_data)
        print(csv_name, "完成且保存！")
        # pd_save_data = pd.DataFrame(np.array([save_data]))
        # pd_save_data.to_csv(r"D:\experiment\result\obs_result\5000_20.csv", index=False, header=False, mode="a")


def predict_one_day(csv_path: str, seq_length: int):
    """
        预测一天的测试集
    :param csv_path: 测试集路径
    :param seq_length: 测试轨迹长度
    :return: 返回一个元组(sum_count,true_count) 总次数和准确次数
    """
    data = np.array(pd.read_csv(csv_path, float_precision="round_trip", header=None))

    csv_name = csv_path.split("\\")[-1]
    s_matrix, e_matrix, t_matrix = get_three_matrix(csv_name)

    # 越界检查使用，没有训练到的数据要进行特殊处理
    emission_bounds = e_matrix.shape[1]  # 获取列数
    section_seq = section(data, seq_length, emission_bounds)
    # 预测总次数
    sum_count = 0
    # 准确次数
    true_count = 0

    for ss in section_seq:
        begin = ss[0]  # 一段轨迹的起始状态
        end = ss[1]  # 一段轨迹的终止状态（预测状态）
        sum_count += 1
        if predict_is_true(s_matrix, e_matrix, t_matrix, data[begin:end]):
            true_count += 1
    return sum_count, true_count


def get_all_observation_sequence(divide, read_path, save_path):
    """
        获取观测矩阵
    :param divide: 分割参数
    :param read_path:
    :param save_path:
    :return:
    """
    csv_data = pd.read_csv(read_path, float_precision="round_trip", index_col=False, usecols=[2, 3])
    cc = sac.create_areas_instance(divide)
    ob_seq = []

    for lo, la in zip(csv_data.lon, csv_data.lat):
        area = cc.divide_area(lo, la)
        ob_seq.append(area)

    pd.DataFrame(ob_seq).to_csv(save_path, index=False, header=False)


def get_all(divide):
    """
        获取测试集的观测状态
    :param divide:
    :return:
    """
    csv_lists = all_csv_file()
    root_path = r"D:\experiment\some"
    save_root_path = os.path.join(r"D:\experiment\obs", 'obs_' + str(divide))
    # 后20天
    for csv_name in csv_lists:
        for day in range(21, 31):
            csv_read_path = os.path.join(root_path, str(day), csv_name)
            csv_save_path = os.path.join(save_root_path, str(day), csv_name)
            if os.path.exists(csv_read_path):
                get_all_observation_sequence(divide, csv_read_path, csv_save_path)
                print(str(divide) + ":第" + str(day) + "天：" + csv_name + "完成")


def predict_is_true(start, emission, transition, observation_seq) -> bool:
    """
        给定观测序列，预测给出最有可能的序列v_sqe，比较v_sqe的最后一个状态和观测序列最后一个状态对应的隐状态是否相同
    :param start: 初始矩阵
    :param emission: 观测矩阵
    :param transition: 隐状态矩阵
    :param observation_seq: 观测序列
    :return:
    """
    p = Predict(start, emission, transition, observation_seq)
    predict_state = p.predict_viterbi()[-1]
    real_state = exchange(observation_seq[-1])
    return predict_state == real_state


def exchange(area):
    """
        根据区域编号查找对应的簇编号
    :param area: 区域编号
    :return:
    """
    path = r"D:\experiment\result\new_some_cluster"
    filename = "res_" + str(divide_parm) + ".csv"
    cells = pd.read_csv(os.path.join(path, filename), header=None)
    # 读取聚类矩阵需要进行翻转
    clusters = np.flipud(np.array(cells)).flatten()
    clusters_num = clusters[area]
    return int(clusters_num)


def test():
    """
        测试函数
    :return:
    """
    start_probability, transition_probability, emission_probability = get_matrix()
    data = pd.read_csv(r"C:\Users\czg\Desktop\10374\obs.csv", header=None, float_precision="round_trip")
    observation_sequence_1d = np.array(data).flatten()
    obs = np.array([observation_sequence_1d[1000:1015]]).T
    isTrue = predict_is_true(start_probability, emission_probability, transition_probability, obs)
    print(isTrue)


def test2():
    path = r"D:\experiment\obs\obs_5000\28\00028.csv"
    dat = read_matrix(path).flatten()
    sets = set()
    for d in dat:
        sets.add(d)
    print(sets)


if __name__ == '__main__':
    # get_all(5000)
    # get_all(3000)
    # test()
    # predict_all_cars(10)
    predict_all_cars(30)
    # print(exchange(337))
    # '00028.csv'
    # index 678 is out of bounds for axis 1 with size 675
    # print(csv_files)
