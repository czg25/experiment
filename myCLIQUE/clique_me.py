import pandas as pd
import numpy as np

"""
    clique 算法的实现
"""


def location_encoding(row, col):
    """
        将二维区域编码成"row-col"
    :param row: 行
    :param col: 列
    :return: "0-1"
    """
    return "".join(str(row) + "-" + str(col))


def location_decoding(loc):
    """

    :param loc: "0-1"
    :return: (0,1)
    """
    temp = loc.split("-")
    return int(temp[0]), int(temp[1])


class CliqueByMe:
    """
        data1 = [[3, 1, 1], [3, 0, 0], [1, 2, 2]]
        a = CliqueByMe(data1, 2)
        a.process()
        res = a.clusters
        print(res)
        print("___________")
        print(a.clusters_to_array())
    """

    def __init__(self, data, threshold):
        self.__data = data
        self.__threshold = threshold
        self.__cell = None
        self.__clusters = []
        self.__row_num = len(self.__data)
        self.__col_num = len(self.__data[0])

    def process(self):
        # 网格初始化
        self.__cell_init()
        self.__allocate_clusters()

    def __cell_init(self):

        self.__cell = np.array([Block() for _ in range(self.__row_num * self.__col_num)]).reshape(
            (self.__row_num, self.__col_num))
        for index_row in range(self.__row_num):
            for index_col in range(self.__col_num):
                self.__cell[index_row][index_col].point_count = self.__data[index_row][index_col]
                self.__cell[index_row][index_col].location_cell = location_encoding(index_row, index_col)

    @property
    def cell(self):
        return self.__cell

    @property
    def clusters(self):
        return self.__clusters

    def __allocate_clusters(self):
        """
         簇计算
        :return:
        """

        # 深度查找
        for row in range(self.__row_num):
            for col in range(self.__col_num):
                if self.__cell[row][col].visit is False:
                    self.__expand(self.__cell[row][col])

    def __expand(self, c):

        c.visit = True

        if c.point_count < self.__threshold:
            # 在这里处理噪声点
            return

        # 获取邻居
        cluster = [c.location_cell]
        neighbors = self.__get__cell_neighbor(c)
        for neighbor in neighbors:
            temp = self.__cell[neighbor[0]][neighbor[1]]
            if temp.point_count >= self.__threshold:
                cluster.append(temp.location_cell)
                neighbors += self.__get__cell_neighbor(temp)

        self.__clusters.append(cluster)

    def __get__cell_neighbor(self, cell):
        """
         获取当前网格的邻居网格
        :param cell: 当前网格
        :return:
        """
        neighbors = []
        temps = cell.get_neighbors(self.__row_num, self.__col_num)
        # 设置这些点已被访问过
        for n in temps:
            if not self.__cell[n[0]][n[1]].visit:
                neighbors.append(n)
                self.__cell[n[0]][n[1]].visit = True
        return neighbors

    def clusters_to_array(self):
        """
            生成的簇集合转成二维列表
        :return:
        """
        if len(self.__clusters) < 0:
            print("clusters is empty")
            return None
        clusters_array = np.zeros((self.__row_num, self.__col_num))
        c_index = 0
        for c in self.__clusters:
            c_index += 1
            for i in c:
                loc_tup = location_decoding(i)
                clusters_array[loc_tup[0], loc_tup[1]] = c_index

        return clusters_array


class Block:
    def __init__(self, count=0, visit=False, location_cell=None):
        self.__location_cell = location_cell or ""
        self.__point_count = count
        self.__visit = visit

    @property
    def location_cell(self):
        return self.__location_cell

    @location_cell.setter
    def location_cell(self, location):
        self.__location_cell = location

    @property
    def visit(self):
        return self.__visit

    @visit.setter
    def visit(self, v):
        self.__visit = v

    @property
    def point_count(self):
        return self.__point_count

    @point_count.setter
    def point_count(self, count):
        self.__point_count = count

    def get_neighbors(self, row_all, col_all):
        """
            获取上下左右的网格编号
        :param row_all:
        :param col_all:
        :return:
        """
        neighbors = []
        cur_row, cur_col = location_decoding(self.__location_cell)
        cur_position = [cur_row, cur_col]
        # 判断运行行还是列
        is_row = True
        for index in range(len(cur_position)):
            if is_row:
                is_row = False
                # 行没超过边界，加入到邻接网格
                if cur_position[index] < row_all - 1:
                    temp_up_row = cur_position[:]
                    temp_up_row[index] += 1
                    neighbors.append(temp_up_row)
            else:
                # 列没超过
                if cur_position[index] < col_all - 1:
                    temp_up_col = cur_position[:]
                    temp_up_col[index] += 1
                    neighbors.append(temp_up_col)
            # 判断下移或者左移是否超过界限
            if cur_position[index] - 1 >= 0:
                temp_down = cur_position[:]
                temp_down[index] -= 1
                neighbors.append(temp_down)
        return neighbors
