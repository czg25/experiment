import os
import numpy as np
import pandas as pd

from prediction.trans_state_matrix import start_matrix, transition_matrix, emission_matrix


def save():
    name = "10374.csv"

    # type_matrix = "start"
    # data = start_matrix(name)

    type_matrix = "emsi"
    data = emission_matrix(name)

    # type_matrix = "trans"
    # data = transition_matrix(name)

    path = r"C:\Users\czg\Desktop\10374"
    path = os.path.join(path, type_matrix + name)
    # 一维的需要转置
    # pd.DataFrame(data).T.to_csv(path, index=False, header=False)
    pd_data = pd.DataFrame(data)
    print(pd_data.shape)
    pd_data.to_csv(path, index=False, header=False)


if __name__ == '__main__':
    save()
