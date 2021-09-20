from pyclustering.cluster.clique import clique, clique_visualizer
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import FCPS_SAMPLES
import numpy as np
import pandas as pd


# 该类无用，测试clique算法

def use_c():
    # read two-dimensional input data 'Target'  sample

    data = read_sample(FCPS_SAMPLES.SAMPLE_TARGET)
    # data = get_data()
    # create CLIQUE algorithm for processing
    intervals = 4  # defines amount of cells in grid in each dimension
    threshold = 100  # lets consider each point as non-outlier
    clique_instance = clique(data, intervals, threshold, ccore=False)

    # start clustering process and obtain results
    clique_instance.process()
    clusters = clique_instance.get_clusters()  # allocated clusters
    noise = clique_instance.get_noise()  # points that are considered as outliers (in this example should be empty)
    cells = clique_instance.get_cells()  # CLIQUE blocks that forms grid

    print("Amount of clusters:", len(clusters))
    print("data_len:", len(data))
    print(len(cells))
    # visualize clustering results
    # clique_visualizer.show_grid(cells, data)  # show grid that has been formed by the algorithm
    # clique_visualizer.show_clusters(data, clusters, noise)  # show clustering results


def get_data():
    path = r"C:\Users\czg\Desktop\10373.csv"
    csv_data = pd.read_csv(path, float_precision="round_trip", index_col=False, usecols=[2, 3])
    return np.array(csv_data)


if __name__ == '__main__':
    use_c()
