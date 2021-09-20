from geopy.distance import great_circle
import math
from areas import prams_process as prams


# 120.852326~122.118227 30.691701~31.874634

class Areas:
    def __init__(self, origin_coordinate, cut_factor, length_width):
        """
        :param origin_coordinate: [lon,lat] 原点坐标值，作为划分网格的起始点
        :param cut_factor: int 分割的距离
        :param length_width:长宽
        """

        self.__origin_coordinate = origin_coordinate
        self.__cut_factor = cut_factor
        self.__length_width = length_width
        self.__cell_lo_count = math.ceil(self.__length_width[0] / self.__cut_factor)
        self.__cell_la_count = math.ceil(self.__length_width[1] / self.__cut_factor)

    def get_cell_count(self) -> list:
        return [self.__cell_lo_count, self.__cell_la_count]

    def divide_area(self, lo, la) -> int:
        """
        根据经纬度返回所在区域的编号
        :return: 编号
        """
        # length = self.__length_width[0]
        # max_lo_count = math.ceil(length / self.__cut_factor)
        # 处理在边界的经纬度
        if lo == self.__origin_coordinate[0] and la >= self.__origin_coordinate[1]:
            temp = math.ceil(
                self.__distance(lo, la, self.__origin_coordinate[0], self.__origin_coordinate[1]) / self.__cut_factor)
            # 在原点
            if temp >= 1:
                return (temp - 1) * self.__cell_lo_count + 1
            elif temp == 0:
                return 1
            else:
                return -1
        elif la == self.__origin_coordinate[1] and lo > self.__origin_coordinate[0]:
            temp = math.ceil(
                self.__distance(lo, la, self.__origin_coordinate[0], self.__origin_coordinate[1]) / self.__cut_factor)
            if temp > 0:
                return temp
            elif temp == 0:
                return 1
            else:
                return -1
        # 处理不在边界
        elif lo > self.__origin_coordinate[0] and la > self.__origin_coordinate[1]:
            # 根据原点坐标做水平投影
            lo_temp = math.ceil(self.__distance(lo, self.__origin_coordinate[1], self.__origin_coordinate[0],
                                                self.__origin_coordinate[1]) / self.__cut_factor)
            la_temp = math.ceil(self.__distance((self.__origin_coordinate[0]), la, self.__origin_coordinate[0],
                                                self.__origin_coordinate[1]) / self.__cut_factor)
            return (la_temp - 1) * self.__cell_lo_count + lo_temp
        else:
            return -1

    def __distance(self, lo, la, lo1, la1):

        point1 = (la, lo)
        point2 = (la1, lo1)
        return great_circle(point1, point2).m

# if __name__ == '__main__':
#     # origin = prams.get_origin()
#     # l_w = prams.get_length_width(prams.range_shanghai())
#     # print(origin, l_w)
#     # a = Areas(origin, 5000, l_w)
#     # print(a.get_cell_count())
#     pass
