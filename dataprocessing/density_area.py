import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle

# import matplotlib.pyplot as plt
from draw import plotting_map


def extract_point():
    """
    该方法处理提取原始数据集中的文件
    :return:
    """
    # 前二十天数据
    need_day = 15
    root_path = r"D:\experiment\some"
    root_path_dir = path_listdir(root_path)
    for sub_path in root_path_dir[0:need_day]:
        # 到r"D:\some\x"目录的路径
        path = os.path.join(root_path, sub_path)
        csv_lists = os.listdir(path)
        for csv_file in csv_lists:
            find_save_point(os.path.join(path, csv_file))


def find_save_point(path):
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False)
    temp_list = []
    for index, row in csv_data.iterrows():
        # 如果速度大于10表示车辆在移动，选取移动车辆的数据
        if float(row[4]) > 10:
            temp_list.append(list(row))

    # 保存
    save_path = r"D:\experiment\density"
    path_split = path.split("\\")
    save_without_filename = os.path.join(save_path, path_split[-2])
    final_save_path = os.path.join(save_without_filename, path_split[-1])
    # 文件夹不存在就创建
    if not os.path.exists(save_without_filename):
        os.makedirs(save_without_filename)
    # 判断车辆是否行驶
    if len(temp_list) > 0:
        pd_df = pd.DataFrame(np.array(temp_list), columns=['id', 'time', 'lon', 'lat', 'speed', "direction"])
        # 删除不需要的行并去重保存
        pd_df.drop(columns=['direction']).drop_duplicates(keep='first', subset=['lon', 'lat']).to_csv(final_save_path,
                                                                                                      index=False)
        print("完成 " + "第" + path_split[-2] + "天 " + path_split[-1] + " 的提取")
    else:
        print("第" + path_split[-2] + "天 " + path_split[-1] + "无有效数据")


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


def drop_dup_data():
    data = pd.read_csv(r"D:\experiment\density\1\00009.csv")
    print(data.count())
    print(data.drop_duplicates(keep='first', subset=['lon', 'lat']))


def point_sum():
    """
    统计所有点的个数 46622341
    :return:
    """
    # path = r"D:\experiment\density"
    path = r"D:\experiment\some_times"
    path_lists = path_listdir(path)
    sum_p = 0
    for sub in path_lists:
        path_1 = os.path.join(path, sub)
        csv_lists = os.listdir(path_1)
        for csv_file in csv_lists:
            df = pd.read_csv(os.path.join(path_1, csv_file))
            sum_p += len(df)
    print(sum_p)


def merge_csv():
    save_path = os.path.join(r"D:\experiment", "new_merge.csv")
    new_df = pd.DataFrame(columns=["id", "time", "lon", "lat", "speed", "direction"])
    new_df.to_csv(save_path, index=False)
    data_path = r"D:\experiment\density"
    for sub_p in path_listdir(data_path)[0:3]:
        csv_path = os.path.join(data_path, sub_p)
        for filename in os.listdir(csv_path):
            df = pd.read_csv(os.path.join(csv_path, filename))
            df.to_csv(save_path, mode='a', index=False, header=False)


def merge_one_csv(csv_name, data_path, save_path):
    """
    合并一辆车20天的数据 00036
    :return:
    """
    print(csv_name, " 合并开始")

    for day in path_listdir(data_path):
        old_csv_path = os.path.join(data_path, day, csv_name)
        df = pd.read_csv(old_csv_path, float_precision="round_trip", index_col=False)
        df.to_csv(save_path, mode="a", index=False, header=False)
    print("合并完成")


def merge_gave_csv():
    """
    指定csv文件
    :return:
    """
    # "00036.csv", "10252.csv","00147.csv" , "10332.csv","10723.csv"

    csv_lists = ["00036.csv"]
    save_path = os.path.join(r"D:\experiment", "one_day.csv")
    data_path = r"D:\experiment\some_times"
    df_column = pd.DataFrame(columns=["id", "time", "lon", "lat", "speed", "direction"])
    df_column.to_csv(save_path, index=False)

    for csv_name in csv_lists:
        merge_one_csv(csv_name, data_path, save_path)


def use_DBSCAN(path_s, points):
    """
    使用DBSCAN密度算法
    :return:
    """
    print("开始聚类")
    path = r"D:\experiment\one_day.csv"
    # path = r"C:\Users\czg\Desktop\00012.csv"
    # path_s = r"D:\experiment\density.csv"
    x = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[2, 3])
    nx = np.array(x)

    model = DBSCAN(eps=1000, min_samples=points, metric=lambda a, b: great_circle(a[::-1], b[::-1]).m)
    model.fit(nx)
    labs = model.labels_
    np.set_printoptions(threshold=10000)
    x["cluster"] = labs
    x.to_csv(path_s, index=False)
    print("聚类结束")


def compute_count():
    """
    计算种类的个数
    :return:
    """
    x = pd.read_csv(r"D:\experiment\one_day.csv", index_col=False, usecols=[2])
    data = []
    for i in np.array(x):
        if i not in data:
            data.append(int(i))
    print(data)
    print(len(data))


def test_dbscan():
    path = r"C:\Users\czg\Desktop\text.csv"
    x = pd.read_csv(path, float_precision="round_trip")
    nx = np.array(x)
    model = DBSCAN(eps=1000, min_samples=1, metric=lambda a, b: great_circle(a[::-1], b[::-1]).m)
    model.fit(nx)
    labs = model.labels_
    # np.set_printoptions(threshold=10000)
    print(labs)


def get_distance(lat, lon):
    print(great_circle((31.04434, 121.469112), (lat, lon)).m)


def C_count():
    path = r"D:\experiment\density.csv"
    data = pd.read_csv(path, float_precision="round_trip")
    c = []
    for i in data.cluster:
        if i not in c:
            c.append(i)
    print(c)


if __name__ == '__main__':
    # extract_point()
    # find_save_point(r"D:\experiment\some\1\00002.csv")
    # compute_count()
    # merge_csv()
    # get_distance(31.043703, 121.468495)
    # get_distance(31.043703, 121.478495)
    # get_distance(31.053703, 121.478495)
    # get_distance(31.053, 121.4666)
    # test_dbscan()
    # merge_gave_csv()
    use_DBSCAN(r"D:\experiment\density_1000_200.csv", 200)
    use_DBSCAN(r"D:\experiment\density_1000_300.csv", 300)
    plotting_map.d_color(r"D:\experiment\density_1000_200.csv", "1000_200.png")
    plotting_map.d_color(r"D:\experiment\density_1000_300.csv", "1000_300.png")
