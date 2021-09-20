import os
import pandas as pd


def one_state(start, csv_name):
    """
    计算单个状态准确率
    :return: 返回正确率
    """
    all_count = 0
    right_count = 0
    root_path = r"E:\state"
    path_listdir = root_path_listdir(root_path)
    for sub_file in path_listdir[(start - 1):]:
        csv_path = os.path.join(root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, index_col=False)
        for index, row in csv_data.iterrows():
            if row[3] != -1 and row[3] == row[1]:
                right_count += 1
            all_count += 1

    if all_count != 0:
        return right_count / all_count
    else:
        return 0


def root_path_listdir(path):
    r_path = path
    root_listdir = os.listdir(r_path)
    root_listdir = list(map(int, root_listdir))
    root_listdir.sort()
    root_listdir = list(map(str, root_listdir))
    return root_listdir


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
    csv_lists = extract_part()
    with open(r"C:\Users\Administrator\Desktop\markrov.txt", mode='w') as f:
        for name in csv_lists:
            a = one_state(day, name)
            print(name, "正确率:", a)
            f.write(str(name) + " 正确率: " + str(a) + "\n")


if __name__ == '__main__':

    # pa = r"E:\state"
    # l = root_path_listdir(pa)
    # df = pd.read_csv(r"C:\Users\Administrator\Desktop\00004 - 副本.csv")
    # a = max(df['speed'])
    # print(a)
    all_data()
