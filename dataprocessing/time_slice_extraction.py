import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from sklearn import metrics
import matplotlib.pyplot as plt


# 时间区间数据提取

def path_listdir(path):
    """
    获取文件路径下的根目录文件名
    :return:
    """
    root_listdir = os.listdir(path)
    root_listdir = list(map(int, root_listdir))
    root_listdir.sort()
    root_listdir = list(map(str, root_listdir))
    return root_listdir


def time_slice(path):
    """
    统计每个时间段的车辆运动情况（单个文件）
    :return: 统计了一个文件中每个小时对应数据的次数
    """
    # path = r"C:\Users\czg\Desktop\00012.csv"
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[1, 4])

    # 保存统计值的数组
    # dict_day = dict.fromkeys([str(i) for i in range(0, 24)], 0)
    arr_day = np.zeros(24)
    for index, row in csv_data.iterrows():
        # 判断速度不为零的,读取的csv_data只有两列
        if float(row[1]) > 10:
            # 分解时间格式00:00:00，取小时
            hour_as_index = row[0].split(":")[0]
            arr_day[int(hour_as_index) - 1] += 1
    # 获取文件名，{filename}
    dict_data = np.array([int(path.split("\\")[-1].split(".")[0])])
    # 合并数组，统计值加入
    # dict_data.update(dict_day)
    return np.concatenate((dict_data, arr_day))


def cycle_all_file():
    """
    循环所有文件
    :return: final_data 运行所有文件后的数据统计数组
    """
    root_path = r"D:\experiment\some"
    # root_path = r"D:\experiment\test"
    sub_root_path = path_listdir(root_path)
    final_data = np.array([])
    # 前20天数据
    for day_lists in sub_root_path[0:20]:
        one_day_csv_path = os.path.join(root_path, day_lists)
        for csv_name in os.listdir(one_day_csv_path):
            dict_data = time_slice(os.path.join(root_path, day_lists, csv_name))
            # 统计数据更新
            final_data = data_integration(final_data, dict_data).copy()
            print("第" + day_lists + "天" + " " + csv_name + "完成")
    return final_data


def data_integration(final_data, temp_data):
    """
    整合数据，叠加次数
    :param final_data: 二维np [标号，0~23]
    :param temp_data: 一维np  [标号，0~23]
    :return: 数据累加后的数组
    """
    # 获取二维数组的第一列
    if len(final_data) > 0:
        first_num = final_data[:, 0]
        if temp_data[0] in first_num:
            # 返回值是列表[[1],type]
            append_index = np.where(first_num == temp_data[0])[0][0]
            for i in range(len(final_data[append_index])):
                if i > 0:
                    final_data[append_index][i] += temp_data[i]
        else:
            final_data = np.vstack((final_data, temp_data))
    else:
        # 如果是第一条数据，直接插入数据
        final_data = temp_data.reshape((1, len(temp_data)))
    return final_data


def record_result():
    """
    保存统计的结果
    :return:
    """
    save_path = r"D:\experiment"
    save_data = cycle_all_file()
    # 设置保存的列名
    save_columns = ["id"] + [str(i) for i in range(0, 24)]
    df = pd.DataFrame(np.array(save_data), columns=save_columns)
    df.to_csv(os.path.join(save_path, "time_analysis.csv"), index=False)


def draw_paint_bar():
    """
    结果 画图 (未完成)
    :return:
    """
    read_path = r"D:\experiment\time_analysis.csv"
    df = pd.read_csv(read_path, float_precision="round_trip", index_col=False, usecols=[i for i in range(1, 25)])

    data = np.array(df)
    x = list(data.sum(axis=0).astype(int))

    y = range(len(x))
    plt.xticks([i for i in range(24)])
    plt.bar(y, x)
    plt.show()


def extract_point(time_zones):
    """
    该方法处理提取原始数据集中的文件
    :param time_zones: 时间区间 [8,9]
    :return:
    """
    # 前二十天数据
    need_day = 20
    root_path = r"D:\experiment\some"
    # root_path = r"D:\experiment\test"
    root_path_dir = path_listdir(root_path)
    for sub_path in root_path_dir[0:20]:
        path = os.path.join(root_path, sub_path)
        csv_lists = os.listdir(path)
        for csv_file in csv_lists:
            find_save(os.path.join(path, csv_file), time_zones)


def find_save(path, time_zones):
    """
        查找符合条件的数据并保存在指定目录
        如果抽取的时间段不存在，则不会保存
    :param path: 文件路径
    :param time_zones: 时间区间
    :return:
    """
    data = []
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False)
    for index, row in csv_data.iterrows():
        # 满足在时间区间的
        if int(row[1].split(":")[0]) in time_zones:
            data.append(list(row))

    # 保存
    save_path = r"D:\experiment\some_times"
    path_split = path.split("\\")
    # 取文件天数编号
    save_without_filename = os.path.join(save_path, path_split[-2])
    # 拼接文件名
    final_save_path = os.path.join(save_without_filename, path_split[-1])

    # 天数文件夹不存在就创建
    if not os.path.exists(save_without_filename):
        os.makedirs(save_without_filename)

    if len(data) > 0:
        pd_df = pd.DataFrame(np.array(data), columns=['id', 'time', 'lon', 'lat', 'speed', "direction"]).to_csv(
            final_save_path, index=False)
        print("完成 " + "第" + path_split[-2] + "天 " + path_split[-1] + " 的提取")
    else:
        print("抽取数据出现错误")


def extract_in_one_min():
    root_path = r"D:\experiment\some"
    root_path_dir = path_listdir(root_path)
    for sub_path in root_path_dir:
        path = os.path.join(root_path, sub_path)
        csv_lists = os.listdir(path)
        for csv_file in csv_lists:
            one_min(os.path.join(path, csv_file))


def one_min(path):
    """
    每一分钟提取一次数据
    :param path:
    :return:
    """
    # 如果改变值了，则是新的一分钟
    minute = -1
    data = []
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False)
    for index, row in csv_data.iterrows():
        temp_minute = int(row[1].split(":")[1])
        if temp_minute != minute:
            data.append(list(row))
            minute = temp_minute

    save_path = r"D:\experiment\123.csv"
    # path_split = path.split("\\")
    # # 取文件天数编号
    # save_without_filename = os.path.join(save_path, path_split[-2])
    # # 拼接文件名
    # final_save_path = os.path.join(save_without_filename, path_split[-1])

    # # 天数文件夹不存在就创建
    # if not os.path.exists(save_without_filename):
    #     os.makedirs(save_without_filename)

    # if len(data) > 0:
    pd_df = pd.DataFrame(np.array(data), columns=['id', 'time', 'lon', 'lat', 'speed', "direction"])
    pd_df.to_csv(save_path, index=False)
    # print("完成 " + "第" + path_split[-2] + "天 " + path_split[-1] + " 的提取")


def find_missing_data():
    """
        统计数据，查看是否完整
    :return:
    """
    csv_count = {}
    # lists = os.listdir(r"D:\experiment\some\1")

    for sub_dir in path_listdir(r"D:\experiment\some_times"):
        path = os.path.join(r"D:\experiment\some_times", sub_dir)
        for cf in os.listdir(path):
            if cf not in csv_count:
                csv_count[cf] = 1
            else:
                csv_count[cf] += 1
    for k in csv_count.items():
        print(k)
    print(len(csv_count))


if __name__ == '__main__':
    # a = np.array([[1, 2, 3],
    #               [4, 5, 6],
    #               [7, 8, 9]])
    # # print(b)
    # # c = np.array([5, 6, 8])
    # # d = np.concatenate((c, b))
    # # print(type(d))
    # b = np.random.uniform(1, 10, 24)
    # b = np.concatenate((np.array([12]), b))
    # b1 = np.random.uniform(1, 10, 24)
    # b1 = np.concatenate((np.array([24]), b1))
    # c = np.array([b, b1])
    # record_result(c)
    extract_point([8, 9, 10, 11, 12, 13, 14])
    # one_min(r"D:\experiment\10373.csv")
