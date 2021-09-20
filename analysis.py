import numpy as np
import pandas as pd
import os


def find_max_state_speed(day, csv_filename):
    """找到每个车的状态最大值"""
    path = r"E:/state"
    path_listdir = root_path_listdir(path)
    max_state = 0
    max_speed = 0
    max_sub = None
    for sub_filename in path_listdir[0:day]:
        csv_path = os.path.join(path, sub_filename, csv_filename)
        csv_data = pd.read_csv(csv_path)
        max_temp_state = max(csv_data['state'])
        max_temp_speed = max(csv_data['ostate'])
        if max_state < max_temp_state:
            max_state = max_temp_state
            max_sub = sub_filename
        if max_speed < max_temp_speed:
            max_speed = max_temp_speed
    print(max_sub)
    return max_state, max_speed


def root_path_listdir(path):
    r_path = path
    root_listdir = os.listdir(r_path)
    root_listdir = list(map(int, root_listdir))
    root_listdir.sort()
    root_listdir = list(map(str, root_listdir))
    return root_listdir


def all_data():
    day = 20
    csv_lists = ['00002.csv', '00004.csv', '00005.csv', '00006.csv', '00007.csv', '00009.csv', '00010.csv']
    for name in csv_lists:
        result = find_max_state_speed(day, name)
        print(name + ":" + "maxstate:" + str(result[0]) + "  " + "maxostate:" + str(result[1]))


if __name__ == '__main__':
    all_data()
