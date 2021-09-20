import numpy as np
import pandas as pd
from hmmlearn import hmm
import numpy

"""

"""


def forward_algorithm(Q, V, A, B, O1, PI):
    """
    前向算法实现
    Q : 隐状态个数
    V : 观测状态
    O1 : 观测序列
    """
    n = Q
    m = len(O1)
    alphas = np.zeros((n, m))
    T = m
    for t in range(T):
        index = V.index(O1[t])
        for i in range(n):
            if t == 0:
                alphas[i][t] = PI[t][i] * B[i][index]
            else:
                alphas[i][t] = np.dot([alpha[t - 1] for alpha in alphas], [a[i] for a in A]) * B[i][index]
    return alphas

