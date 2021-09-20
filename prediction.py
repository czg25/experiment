import os
import pandas as pd
import numpy as np
from hmmlearn import hmm
import warnings
np.set_printoptions(threshold=1000000)





def traversal_state(column, count_loop, csv_name):
    # 观测矩阵有问题得重写
    """根据不同列来计算状态矩阵"""
    tran_state = 'state'
    emis_state = 'ostate'

    max_row = get_max_state(count_loop, csv_name)
    # 列索引
    if column == tran_state:
        state_index = 1
        state_matrix = np.zeros((max_row, max_row))
        matrix_save_path = r"E:\matrix\state"

    # 观测状态手动输入
    elif column == emis_state:
        state_index = 2
        # 观测状态的行由隐状态的行来决定
        state_matrix = np.zeros((max_row, 6))
        matrix_save_path = r"E:\matrix\speed"
    else:
        print("列名不存在")
        return

    # 状态矩阵初始化

    # 遍历数据
    root_path = r"E:\state"
    root_listdir = root_path_listdir()
    for sub_file in root_listdir[0:count_loop]:
        if state_matrix is None:
            print("矩阵为空，出错了")
            return
        first_flag = True
        last_data = 1
        csv_path = os.path.join(root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, index_col=False)
        for index, row in csv_data.iterrows():
            if column == tran_state:
                if first_flag:
                    last_data = row[state_index]
                    first_flag = False
                else:
                    state_matrix[last_data - 1][row[state_index] - 1] += 1
                    last_data = row[state_index]
            elif column == emis_state:
                state_matrix[row[state_index - 1] - 1][row[state_index] - 1] += 1

    # 根据统计的矩阵，计算转移概率矩阵
    sum_row = np.sum(state_matrix, axis=1)
    # count 记录所遍历的行
    count = 0
    for row in state_matrix:
        for i in range(len(row)):
            if sum_row[count] == 0:
                if count != i:
                    state_matrix[count][i] = 0
                else:
                    state_matrix[count][i] = 1
            else:
                state_matrix[count][i] /= sum_row[count]
        count += 1
    # 处理完成后对状态矩阵进行保存
    df_matrix = pd.DataFrame(state_matrix)
    df_matrix.to_csv(matrix_save_path, index=False, header=False)

    return state_matrix


def get_traversal_state(column, count_loop, csv_name):
    """
        将训练的状态矩阵保存
    :param column:
    :param count_loop:
    :param csv_name:
    :return:
    """
    tran_state = 'state'
    emis_state = 'ostate'

    # 矩阵保存路径

    # 转移矩阵
    if column == tran_state:
        state_path = os.path.join(r"E:\matrix\state", csv_name)
        if os.path.exists(state_path):
            state_matrix = pd.read_csv(state_path, index_col=False, float_precision="round_trip", header=None)
            if len(state_matrix) > 0:
                return np.array(state_matrix)
            else:
                return traversal_state(column, count_loop, csv_name)
        else:
            return traversal_state(column, count_loop, csv_name)

    elif column == emis_state:
        speed_path = os.path.join(r"E:\matrix\speed", csv_name)
        if os.path.exists(speed_path):
            state_matrix = pd.read_csv(speed_path, index_col=False, float_precision="round_trip", header=False)
            if len(state_matrix) > 0:
                return np.array(state_matrix)
            else:
                return traversal_state(column, count_loop, csv_name)
        else:
            return traversal_state(column, count_loop, csv_name)

    else:
        print("列名不存在")
        return


def get_max_state(count_loop, csv_name):
    """获取目的最大状态值来决定转移矩阵的行数"""
    max_value = 0
    root_path = r"E:\state"
    root_listdir = root_path_listdir()
    for sub_file in root_listdir[0:count_loop]:
        csv_path = os.path.join(root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, index_col=False)
        for index, row in csv_data.iterrows():
            if max_value < row[1]:
                max_value = row[1]
    return max_value


def get_start_probability(count_loop, csv_name):
    """计算初始隐状态概率矩阵"""
    start_save_path = r"E:\matrix\start"
    if os.path.exists(os.path.join(start_save_path, csv_name)):
        read_start_pro = pd.read_csv(os.path.join(start_save_path, csv_name), index_col=False,
                                     float_precision="round_trip",
                                     header=None)
        # flatten()可以将读取的二维降到一维
        return np.array(read_start_pro).flatten()
    else:
        # 如果不存在则将数据进行读取训练并保存

        # 获取最大行数
        max_row = get_max_state(count_loop, csv_name)
        start_pro = np.zeros(max_row)

        root_path = r"E:\state"
        root_listdir = root_path_listdir()
        for sub_file in root_listdir[0:count_loop]:
            csv_path = os.path.join(root_path, sub_file, csv_name)
            csv_data = pd.read_csv(csv_path, index_col=False)

            for index, row in csv_data.iterrows():
                ind = row[1] - 1
                start_pro[ind] += 1

        sum_state = start_pro.sum()
        for i in range(len(start_pro)):
            start_pro[i] /= sum_state

        # 保存
        df = pd.DataFrame(start_pro)
        df.to_csv(os.path.join(start_save_path, csv_name), index=False, header=False)
        return start_pro


def use_forward(start_probability, transition_probability, emission_probability, observation_sequence):

    """
    使用前向算法
    :return: 最大数值
    """
    states_num = len(start_probability)
    # 初始状态转换为二维矩阵 [[]]
    start_probability = np.array(start_probability).reshape(1, states_num)
    # 观测矩阵手动输入
    observations = ['0', '1', '2', '3', '4', '5']
    alphas = forward_algorithm(states_num, observations, transition_probability, emission_probability,
                               observation_sequence, start_probability)
    # print(alphas)
    predict_array = np.zeros((1, states_num))
    # 各个状态的前向概率乘上下一个概率的积的和
    for i in range(len(predict_array)):
        for j in range(states_num):
            predict_array[i][j] = np.dot([alpha[-1] for alpha in alphas], [tp[j] for tp in transition_probability])
    # 返回概率最大的状态
    return np.argmax(predict_array) + 1


def use_viterbi_forward(count_loop, end_loop, csv_name, algorithm):

    # 观测值录入有问题，要录入字符类型，且列号索引不对
    """
    根据前向算法或者后向算法来预测数据
    :param count_loop:
    :param end_loop:
    :param csv_name:
    :param algorithm:
    :return:
    """

    # 获取三个矩阵
    start_probability = get_start_probability(count_loop, csv_name)
    transition_probability = get_traversal_state("state", count_loop, csv_name)
    emission_probability = traversal_state("ostate", count_loop, csv_name)

    observation_sequence = []
    save_prediction_data = []
    root_path = r"E:\state"
    root_listdir = root_path_listdir()
    for sub_file in root_listdir[count_loop: end_loop]:
        # 读取路径
        csv_path = os.path.join(root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, index_col=False)

        for index, row in csv_data.iterrows():
            os_length = len(observation_sequence)
            # 如果观测序列为零，先加入观测序列
            if os_length == 0:
                observation_sequence.append(row[1] - 1)
            elif os_length > 0:
                # 如果观测序列大于零且大于50，则取最后五十个数据
                if os_length > 50:
                    observation_sequence = observation_sequence[-50:]

                if algorithm == "viterbi":
                    next_state = viterbi_algorithm(start_probability, transition_probability, emission_probability,
                                                   np.array(observation_sequence))
                    save_prediction_data.append([row[0], row[1], row[2], next_state])
                elif algorithm == "forward":
                    next_state = use_forward(start_probability, transition_probability, emission_probability,
                                             np.array(observation_sequence))
                    save_prediction_data.append([row[0], row[1], row[2], next_state])
                else:
                    print("算法错误")
                    return
                # 添加一个观测序列
                observation_sequence.append(row[1] - 1)
        df = pd.DataFrame(np.array(save_prediction_data), columns=['time', 'state', 'ostate', 'prediction'])
        df.to_csv(csv_path, index=False)


def viterbi_algorithm(start_probability, transition_probability, emission_probability, observation_sequence):
    """
    维特比算法
    :param start_probability: 初始矩阵
    :param transition_probability: 转移矩阵
    :param emission_probability: 观测状态的发射矩阵
    :param observation_sequence: 观测序列
    :return: 返回预测值
    """
    n = len(start_probability)
    model = hmm.MultinomialHMM(n_components=n)
    model.startprob_ = start_probability
    model.transmat_ = transition_probability
    model.emissionprob_ = emission_probability
    log_prob, result = model.decode(observation_sequence, algorithm="viterbi")
    return result


def markov_algorithm(state, transition_probability):
    """
    马尔可夫
    :param state:状态序号
    :param transition_probability:转移矩阵
    :return: 预测序号
    """
    # 防止不在预测范围内的情况出现
    if state > len(transition_probability):
        return -2
    else:
        return np.argmax(transition_probability[(state - 1)]) + 1


def forward_algorithm(Q, V, A, B, O1, PI):
    """
    前向算法实现
    Q : 隐状态个数
    V : 观测状态
    O1 : 观测序列
    """
    n = Q
    m = len(O1)
    alphas = np.zeros((n, m))
    T = m
    for t in range(T):
        index = V.index(O1[t])
        for i in range(n):
            if t == 0:
                alphas[i][t] = PI[t][i] * B[i][index]
            else:
                alphas[i][t] = np.dot([alpha[t - 1] for alpha in alphas], [a[i] for a in A]) * B[i][index]
    return alphas


def root_path_listdir():
    r_path = r"E:\state"
    root_listdir = os.listdir(r_path)
    root_listdir = list(map(int, root_listdir))
    root_listdir.sort()
    root_listdir = list(map(str, root_listdir))
    return root_listdir


def use_markov(state, count_loop, end_loop, csv_name):
    """
    使用马尔可夫预测
    :param state: 字符类型，需要预测的列
    :param count_loop: 训练天数
    :param end_loop: 测试天数
    :param csv_name: csv文件名
    """
    if state == "state":
        state_index = 1
    elif state == "ostate":
        state_index = 2
    else:
        print("状态输入错误！")
        return

    transition_probability = get_traversal_state(state, count_loop, csv_name)

    root_path = r"E:\state"
    root_listdir = root_path_listdir()
    for sub_file in root_listdir[count_loop: end_loop]:
        # 保存的数据
        save_prediction_data = []
        # 上一个状态状态
        cur_state = None
        # 标记为第一次记录
        first_flag = True
        csv_path = os.path.join(root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, index_col=False)
        # 遍历每天的文件，这个地方可以进行文件处理
        for index, row in csv_data.iterrows():
            # 第一天数据不进行预测
            if first_flag:
                cur_state = row[state_index]
                first_flag = False
            else:
                next_state = markov_algorithm(int(cur_state), transition_probability)
                save_prediction_data.append([row[0], row[1], row[2], next_state])
                cur_state = row[state_index]

        df = pd.DataFrame(np.array(save_prediction_data), columns=['time', 'state', 'ostate', 'prediction'])
        df.to_csv(csv_path, index=False, mode='w')


def extract_part():
    path = r"D:\input\1"
    dir_list = os.listdir(path)
    r_list = []
    i = 0
    for name in dir_list:
        if i < 1000:
            r_list.append(name)
        i += 1
    return r_list


def all_data():
    day = 20
    # '00002.csv','00004.csv', '00005.csv', '00006.csv', '00007.csv', '00009.csv', '00010.csv'
    # csv_lists = extract_part()
    csv_lists = ['00005.csv']
    for name in csv_lists:
        # use_markov("state", 20, 30, name)
        use_viterbi_forward(20, 21, name, "viterbi")
        # use_viterbi_forward(20, 30, name, "forward")
        print(name, "处理完成！")


if __name__ == '__main__':
    # print(get_start_probability(1, "123.csv"))
    # print(traversal_state("ostate", 1, "123.csv"))
    # test()
    # all_data()
    a = get_traversal_state('state', 20, '00005.csv')
    print(a)
