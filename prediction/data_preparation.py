import numpy as np
import pandas as pd
import os


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


def get_cluster_data(divide_pram) -> np:
    """
        获取聚类数据
    :return:
    """
    root_path = r"D:\experiment\result\new_some"
    path = os.path.join(root_path, "res_" + str(divide_pram) + ".csv")
    data = pd.read_csv(path, header=None)
    return np.array(data)


if __name__ == '__main__':
    print(get_cluster_data(5000))
