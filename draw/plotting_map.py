from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import GeoType
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
import webbrowser


# 更新地图
# pip install echarts-china-provinces-pypkg
# pip install echarts-china-cities-pypkg


def draw_point():
    # 初始化
    g = Geo()
    g.add_schema(maptype='上海')
    data_pair = []
    print("正在绘制.......")
    df = pd.read_csv(r"C:\Users\czg\Desktop\00012.csv", float_precision="round_trip", index_col=False)

    for index, row in df.iterrows():
        g.add_coordinate(index, row[2], row[3])
        data_pair.append((index, index))

    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=2)
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False), type='scatter')
    g.render('test_render11111.html')
    print("绘制完成.......")


def plt_point():
    # path = r"D:\experiment\one_day.csv"
    path = r"C:\Users\czg\Desktop\00012.csv"
    df = pd.read_csv(path, float_precision="round_trip", index_col=False)
    # 第一个参数指定行，第二个指定列
    x = df.loc[0:, "lon":"lon"].values
    y = df.loc[0:, "lat":"lat"].values
    plt.figure(figsize=(10, 8), dpi=300)
    plt.xlabel("lon")
    plt.ylabel("lat")
    # plt.scatter(x, y, marker=".")
    plt.scatter(x, y, marker=".", s=1)
    plt.savefig(fname="pic.png")
    plt.show()


def use_folium():
    points = folium.map.FeatureGroup()
    points1 = folium.map.FeatureGroup()
    data = pd.read_csv(r"C:\Users\czg\Desktop\00012.csv", float_precision="round_trip", index_col=False)
    data1 = data[1:4000]
    data2 = data[4000:]
    for lon, lat in zip(data1.lon, data1.lat):
        points.add_child(
            folium.CircleMarker(
                (lat, lon),
                radius=1,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.4
            )
        )

    for lon, lat in zip(data2.lon, data2.lat):
        points1.add_child(
            folium.CircleMarker(
                (lat, lon),
                radius=1,
                color="green",
                fill=True,
                fill_color="green",
                fill_opacity=0.4
            )
        )

    show_map = folium.Map(location=[31.193697, 121.563727])
    show_map.add_child(points)
    show_map.add_child(points1)
    show_map.save("w1.html")
    webbrowser.open("../w1.html")


def usef():
    points = folium.map.FeatureGroup()
    data = pd.read_csv(r"C:\Users\czg\Desktop\10374\test\10374_25.csv", float_precision="round_trip", index_col=False)
    for lon, lat in zip(data.lon, data.lat):
        points.add_child(
            folium.CircleMarker(
                (lat, lon),
                radius=1,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.4
            )
        )
    show_map = folium.Map(location=[31.193697, 121.563727])
    show_map.add_child(points)
    show_map.save("10373.html")
    webbrowser.open("10373.html")


def different_color():
    # path = r"C:\Users\czg\Desktop\text.csv"
    path = r"D:\experiment\density.csv"
    data = pd.read_csv(path, float_precision="round_trip")
    # c为簇的个数
    c = ['c', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w',
         '#00FF00',
         '#32CD32',
         '#FAF0E6',
         '#FF00FF',
         '#800000',
         '#66CDAA',
         '#0000CD',
         '#BA55D3',
         '#9370DB',
         '#3CB371',
         '#7B68EE',
         '#00FA9A',
         '#48D1CC',
         '#C71585',
         '#191970',
         '#F5FFFA',
         '#FFE4E1',
         '#FFE4B5',
         '#FFDEAD',
         '#000080',
         '#FDF5E6',
         ]

    # for i in data.cluster:
    #     if i not in c:
    #         c.append(i)
    # print(c)

    # x = data.loc[0:, "lon":"lon"].values
    # y = data.loc[0:, "lat":"lat"].values
    fig = plt.figure(figsize=(10, 8), dpi=300)
    axes = fig.add_subplot(111)
    i = 0
    for index, row in data.iterrows():
        axes.scatter(row[0], row[1], c=c[int(row[2]) + 2], s=1)
        print(i)
        i += 1
    plt.xlabel("lon")
    plt.ylabel("lat")
    plt.savefig(fname="dc.png")
    plt.show()


def d_color(path, name):
    # path = r"C:\Users\czg\Desktop\text.csv"
    # path = r"D:\experiment\density.csv"
    data = pd.read_csv(path, float_precision="round_trip")
    # c为簇的个数
    c = ['c', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w',
         '#00FF00',
         '#32CD32',
         '#FAF0E6',
         '#FF00FF',
         '#800000',
         '#66CDAA',
         '#0000CD',
         '#BA55D3',
         '#9370DB',
         '#3CB371',
         '#7B68EE',
         '#00FA9A',
         '#48D1CC',
         '#C71585',
         '#191970',
         '#F5FFFA',
         '#FFE4E1',
         '#FFE4B5',
         '#FFDEAD',
         '#000080',
         '#FDF5E6',
         ]

    # for i in data.cluster:
    #     if i not in c:
    #         c.append(i)
    # print(c)

    # x = data.loc[0:, "lon":"lon"].values
    # y = data.loc[0:, "lat":"lat"].values
    fig = plt.figure(figsize=(10, 8), dpi=300)
    axes = fig.add_subplot(111)
    i = 0
    for index, row in data.iterrows():
        axes.scatter(row[0], row[1], c=c[int(row[2]) + 2], s=1)
        print(i)
        i += 1
    plt.xlabel("lon")
    plt.ylabel("lat")
    plt.savefig(fname=name)
    plt.show()


def get_map():
    data = pd.read_csv(path)


if __name__ == '__main__':
    usef()
