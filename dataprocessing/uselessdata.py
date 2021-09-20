import pandas as pd
import os
import shutil as st


def statistical_days():
    """统计每辆车是否有完整的30天数据，数据生成文本"""
    path = r"D:\input"
    root_list = os.listdir(path)

    csv_name_lists = {}
    with open(r"C:\Users\Administrator\Desktop\123.txt", "w", encoding='utf-8') as f:
        for subdir in root_list:
            sub_path = os.path.join(path, subdir)
            for i in os.listdir(sub_path):
                if i.strip() not in csv_name_lists.keys():
                    csv_name_lists.update({i.strip(): 1})
                else:
                    csv_name_lists[i.strip()] += 1
            print("处理" + subdir + "完成")
        for key, value in csv_name_lists.items():
            f.write(key + ',' + str(value) + '\n')


def check_car_data():
    """总共数据13832
       30天完整数据为13182
    """
    txt_content = {}
    for i in open(r"C:\Users\Administrator\Desktop\123.txt", "r", encoding='utf-8'):
        line = i.split(',')
        txt_content.update({line[0]: int(line[1].strip())})
    # [30, 26, 29, 16, 28, 27, 25, 24, 21, 19, 23, 22, 17, 20, 12, 18, 1, 2, 14, 6, 11, 8, 9, 13, 15, 10, 5, 4, 7]
    day_list = {}
    for value in txt_content.values():
        if str(value) not in day_list.keys():
            day_list.update({str(value): 1})
        else:
            day_list[str(value)] += 1
    for k, v in day_list.items():
        print(k + ":" + str(v))


def del_car_data():
    # 需要删除的列表 650
    del_list = []
    with open(r"C:\Users\Administrator\Desktop\123.txt", "r", encoding='utf-8') as f:
        for i in f:
            line = i.split(",")
            if int(line[1]) != 30:
                del_list.append(line[0])
    print(del_list)
    print(len(del_list))

    # 删除
    path = r"D:\input"
    path_lists = os.listdir(path)
    for sub_filename in path_lists:
        subdir_path = os.path.join(path, sub_filename)
        for del_csv in os.listdir(subdir_path):
            if del_csv in del_list:
                os.remove(os.path.join(subdir_path, del_csv))
                print("删除成功：", del_csv)


def del_repeating_data():
    df = pd.read_csv(r"C:\Users\Administrator\Desktop\00004.csv")
    df.drop_duplicates(subset=['lon', 'lat', 'speed'], keep='first', inplace=True)
    df.to_csv(r"C:\Users\Administrator\Desktop\00004.csv", mode="w", index=False)


def extract():
    csv_list = extract_part()
    path = r"D:\input"
    root_copy_path = r"E:\some"
    # 生成子目录
    for i in range(1, 31):
        os.makedirs(os.path.join(root_copy_path, str(i)))

    for sub_root_name in os.listdir(path):
        sub_path = os.path.join(path, sub_root_name)
        copy_path = os.path.join(root_copy_path, sub_root_name)
        for csv_file in os.listdir(sub_path):
            if csv_file in csv_list:
                st.copy(os.path.join(sub_path, csv_file), os.path.join(copy_path, csv_file))


def del_all_data():
    # 删除文件夹下的数据
    path = r"E:\some"
    st.rmtree(path)
    for i in range(1, 31):
        os.makedirs(os.path.join(path, str(i)))


def find_useful_date():
    df = pd.read_csv(r"C:\Users\Administrator\Desktop\00004 - 副本.csv")
    df = df[df['speed'] >= 10]
    df.drop_duplicates()
    print(df)


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


if __name__ == '__main__':
    # statistical_days()
    # del_car_data()
    # del_repeating_data()
    # del_all_data()
    # find_useful_date()
    # extract_part()
    extract()
    # calculatestate.f()
