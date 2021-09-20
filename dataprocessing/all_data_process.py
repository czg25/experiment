import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from sklearn import metrics
from dataprocessing import time_slice_extraction as tse


def path_listdir(path):
    """
    获取路径下的所有文件名
    :param path:
    :return: 列表
    """
    return tse.path_listdir(path)


def through_all_data():
    root_path = r"D:\experiment\some"
    sub_root_path = path_listdir(root_path)
    save_path = r"D:\experiment\all.csv"
    if not os.path.exists(save_path):
        print("运行到了初次创建")
        new_df = pd.DataFrame(columns=["id", "time", "lon", "lat", "speed"])
        new_df.to_csv(save_path, index=False)

    # 访问的文件命列表
    temp_listdir = ["10799.csv", "10444.csv", "10868.csv", "10535.csv", "00089.csv"]
    for day_lists in sub_root_path[0:20]:
        one_day_csv_path = os.path.join(root_path, day_lists)
        for csv_name in temp_listdir:
            update_delete_csvInfo(os.path.join(one_day_csv_path, csv_name), csv_name)


def update_delete_csvInfo(path, csv_name):
    """
    处理id,读取需要的列
    添加到指定 csv下
    :param csv_name:
    :param path:
    :return:
    """
    save_path = r"D:\experiment\all.csv"
    path_split = path.split("\\")

    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[0, 1, 2, 3, 4])
    # 处理id，会舍弃前面补位的零
    name = int(csv_name.split(".")[0])
    csv_data.loc[:, "id"] = name

    # 保存
    pd.DataFrame(np.array(csv_data), columns=['id', 'time', 'lon', 'lat', 'speed']).to_csv(
        save_path, mode="a", index=False, header=False)
    print("完成 " + "第" + path_split[-2] + "天 " + path_split[-1] + " 的提取")


if __name__ == '__main__':
    through_all_data()
