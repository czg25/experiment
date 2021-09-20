from geopy.distance import great_circle
import math
import os
import numpy as np
import pandas as pd
import prediction
import calculate_precision as cp

"""
    暂时弃用
"""


def read_min_max(csv_name):
    """获取最大最小经纬度"""
    read_data = pd.read_csv(os.path.join(r"E:\min_max", csv_name), float_precision="round_trip")
    return np.array(read_data, dtype=np.float64)


def find_save(csv_name, count_loop):
    """查找并保存最大最小经纬度
          # [min lon
             min lat
             max lon
             max lat
            ]
    """
    # 防止读取浮点数时，出现31.0770619999999998这种问题，在读取csv文件是需要加上float_precision="round_trip"
    min_max_data = np.zeros([4, 2], dtype=np.float64)
    root_path = r"E:\some"
    first_flag = True
    root_path_listdir = os.listdir(root_path)
    root_path_listdir = list(map(int, root_path_listdir))
    root_path_listdir.sort()
    root_path_listdir = list(map(str, root_path_listdir))

    for sub_file in root_path_listdir[0:count_loop]:
        csv_path = os.path.join(root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, float_precision="round_trip")

        min_lon = np.array(csv_data.loc[csv_data['lon'].idxmin()])[2:4]
        min_lat = np.array(csv_data.loc[csv_data['lat'].idxmin()])[2:4]
        max_lon = np.array(csv_data.loc[csv_data['lon'].idxmax()])[2:4]
        max_lat = np.array(csv_data.loc[csv_data['lat'].idxmax()])[2:4]
        if first_flag:
            min_max_data = np.array([min_lon, min_lat, max_lon, max_lat])
            first_flag = False
        else:
            if (not judge_max(min_lon[0], min_max_data[0][0])) and min_max_data[2][0] > 0:
                min_max_data[0] = min_lon
            if (not judge_max(min_lat[1], min_max_data[1][1])) and min_max_data[3][1] > 0:
                min_max_data[1] = min_lat
            if judge_max(max_lon[0], min_max_data[2][0]):
                min_max_data[2] = max_lon
            if judge_max(max_lat[1], min_max_data[3][1]):
                min_max_data[3] = max_lat

    write_data = pd.DataFrame(min_max_data, columns=['lon', 'lat'])
    write_data.to_csv(os.path.join(r'E:\min_max', csv_name), index=False)


def judge_max(new, old):
    # 旧值大于新值，返回true，否则false
    return True if (old < new) else False


def gsp_distance(lo, la, lo1, la1):
    point1 = (la, lo)
    point2 = (la1, lo1)
    return great_circle(point1, point2).m


def divide_area(lo, la, length_width, origin):
    """计算该点的所在的区域
        lo,la 需为float类型
    """
    cut_factor = 5000.00
    length = float(length_width[0])
    max_lo_count = math.ceil(length / cut_factor)
    # 处理在边界的经纬度
    if float(lo) == origin[0] and la >= origin[1]:
        temp = math.ceil(gsp_distance(lo, la, origin[0], origin[1]) / cut_factor)
        # 在原点
        if temp >= 1:
            return (temp - 1) * max_lo_count + 1
        elif temp == 0:
            return 1
        else:
            return -1
    elif float(la) == origin[1] and float(lo) > origin[0]:
        temp = math.ceil(gsp_distance(lo, la, origin[0], origin[1]) / cut_factor)
        if temp > 0:
            return temp
        elif temp == 0:
            return 1
        else:
            return -1
    # 处理不在边界
    elif float(lo) > origin[0] and float(la) > origin[1]:
        lo_temp = math.ceil(gsp_distance(lo, origin[1], origin[0], origin[1]) / cut_factor)
        la_temp = math.ceil(gsp_distance((origin[0]), la, origin[0], origin[1]) / cut_factor)
        return (la_temp - 1) * max_lo_count + lo_temp
    else:
        return -1


def length_side(min_max_result):
    """计算长和宽"""
    result = []
    length = gsp_distance(min_max_result[0][0], min_max_result[0][1], min_max_result[2][0], min_max_result[0][1])
    width = gsp_distance(min_max_result[1][0], min_max_result[1][1], min_max_result[1][0], min_max_result[3][1])
    result.append(length)
    result.append(width)
    return result


def get_min_lon_lat(col, min_lo_la, count_loop, file_name):
    """遍历所有文件夹下的文件，找出极值经纬度"""
    data_min = np.zeros(2, dtype=np.float64)
    print("get_min_lon_lat中的min_lo_la", min_lo_la)

    root_path = r"E:\some"
    root_path_listdir = os.listdir(root_path)
    root_path_listdir = list(map(int, root_path_listdir))
    root_path_listdir.sort()
    root_path_listdir = list(map(str, root_path_listdir))

    for sub_file in root_path_listdir[0:count_loop]:
        csv_path = os.path.join(root_path, sub_file, file_name)
        csv_data = pd.read_csv(csv_path, encoding='utf-8', index_col=False, float_precision="round_trip")
        if col == 'lon':
            # get最小值所对应的行·
            extract_data = csv_data.loc[csv_data[col] == min_lo_la[0]]
            # 查找的最小值如果在当前文件中，否则执行下一个文件
            if len(extract_data) > 0:
                # 取最小经度中的最小纬度
                temp_min = np.min(np.array(extract_data[['lon', 'lat']]), axis=0)
                if data_min[1] != 0 and (temp_min[1] < data_min[1]):
                    data_min[1] = temp_min[1]
                # 第一次记录
                elif data_min[0] == 0 and data_min[0] == 0:
                    data_min[0] = temp_min[0]
                    data_min[1] = temp_min[1]

        elif col == 'lat':
            extract_data = csv_data.loc[csv_data[col] == min_lo_la[1]]
            if len(extract_data) > 0:

                temp_min = np.max(np.array(extract_data[['lon', 'lat']]), axis=0)
                if data_min[0] != 0 and (temp_min[1] > data_min[1]):
                    data_min[0] = float(temp_min[0])
                elif data_min[1] == 0:
                    data_min[0] = float(temp_min[0])
                    data_min[1] = float(temp_min[1])
        else:
            print("列名错误")
    return data_min


def get_origin(min_max_result, count_loop, file_name):
    """获取原点"""
    origin = []
    # print(" min_max_result[0] = ", min_max_result[0])
    # print(" min_max_result[1] = ", min_max_result[1])

    lon_min = get_min_lon_lat('lon', min_max_result[0], count_loop, file_name)
    lat_min = get_min_lon_lat('lat', min_max_result[1], count_loop, file_name)
    # print("lon_min=", lon_min)
    # print("lat_min=", lat_min)
    if float(lon_min[0]) <= float(lat_min[0]):
        origin.append(float(lon_min[0]))
    else:
        origin.append(float(lat_min[0]))

    if float(lon_min[1]) <= float(lat_min[1]):
        origin.append(float(lon_min[1]))
    else:
        origin.append(float(lat_min[1]))
    return origin


def save_state(csv_name, count_loop):
    """
        预测下一个地点
    :param csv_name:
    :param count_loop:
    :return:
    """
    root_path = r"E:\some"
    save_root_path = r"E:\state"
    root_path_listdir = os.listdir(root_path)
    root_path_listdir = list(map(int, root_path_listdir))
    root_path_listdir.sort()
    root_path_listdir = list(map(str, root_path_listdir))

    # 获取原点
    min_max_lo_la = read_min_max(csv_name)
    origin = get_origin(min_max_lo_la, count_loop, csv_name)
    # 获取最大宽度和高度
    l_w = length_side(min_max_lo_la)
    for sub_file in root_path_listdir[0:count_loop]:
        list_data = []
        csv_path = os.path.join(root_path, sub_file, csv_name)
        save_path = os.path.join(save_root_path, sub_file, csv_name)
        csv_data = pd.read_csv(csv_path, encoding='utf-8')
        for index, row in csv_data.iterrows():
            state = divide_area(row[2], row[3], l_w, origin)
            o_state = speed_state(row[4])
            list_data.append([row[1], state, o_state, -1])
        pd_df = pd.DataFrame(np.array(list_data), columns=['time', 'state', 'ostate', 'prediction'])
        pd_df.to_csv(save_path, index=False)
        print(csv_name + "处理完成")


def speed_state(speed):
    if speed < 10:
        return 0
    elif 10 <= speed < 20:
        return 1
    elif 20 <= speed < 30:
        return 2
    elif 30 <= speed < 40:
        return 3
    elif 40 <= speed < 50:
        return 4
    elif speed >= 50:
        return 5
    else:
        return -1


def data_request():
    # 需要处理的车辆文件名

    csv_list = extract_part()
    return csv_list


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
    """
    遍历循环所有文件数据
    :return:
    """

    day = 30
    request_file = data_request()
    for filename in request_file:
        find_save(filename, day)
        print("完成极值寻找:" + filename)
        save_state(filename, day)
        print("完成区域划分:" + filename)


def f():
    all_data()
    # prediction.all_data()
    # cp.all_data()


if __name__ == '__main__':
    """
        首先运行，计算区域位置
    """
    # find_save('00002.csv', 20)
    # red = read_min_max('00005.csv')
    # print("red=", red)
    # ad = get_origin(red, 20, "00005.csv")
    # print(ad)
    # df = pd.read_csv(r"C:\Users\Administrator\Desktop\123.csv",index_col=False)
    # x = df.loc[df['lon'] == 12.6]
    # print(x)
    # print(len(x))
    # a = np.min(np.array(x[['lon', 'lat']]), axis=0)
    # print(a)
    f()
