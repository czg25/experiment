import os
import numpy as np
import pandas as pd

from dataprocessing.time_slice_extraction import path_listdir, one_min


def one_minute_data():
    """
        数据提取成每分钟一次
    :return:
    """
    root_path = r"D:\experiment\some"
    root_path_dir = path_listdir(root_path)
    test_day = [root_path_dir[24]]
    for sub_path in test_day:
        path = os.path.join(root_path, sub_path)
        csv_lists = os.listdir(path)
        for csv_file in csv_lists:
            csv_path = os.path.join(path, csv_file)

            # 如果改变值了，则是新的一分钟
            minute = -1
            data = []
            csv_data = pd.read_csv(csv_path, float_precision="round_trip", index_col=False)
            for index, row in csv_data.iterrows():
                temp_minute = int(row[1].split(":")[1])
                if temp_minute != minute:
                    data.append(list(row))
                    minute = temp_minute

            save_path = r"D:\experiment\assign_task\test"
            path_split = csv_path.split("\\")
            # 取文件天数编号
            save_without_filename = os.path.join(save_path, path_split[-2])
            # 拼接文件名
            final_save_path = os.path.join(save_without_filename, path_split[-1])

            # 天数文件夹不存在就创建
            if not os.path.exists(save_without_filename):
                os.makedirs(save_without_filename)

            # if len(data) > 0:
            pd_df = pd.DataFrame(np.array(data), columns=['id', 'time', 'lon', 'lat', 'speed', "direction"])
            pd_df.to_csv(final_save_path, index=False)
            print("完成 " + "第" + path_split[-2] + "天 " + path_split[-1] + " 的提取")


def get_vehicle():
    pass


if __name__ == '__main__':
    one_minute_data()
