import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from hmmlearn import hmm
from areas import statistics_all_car as sac
from prediction.all_trans_save import read_matrix

"""
    输入矩阵，封装预测算法
"""


class Predict:
    def __init__(self, start_pro, emission_pro, transition_pro, observation_sqe):
        self.__start_pro = start_pro
        self.__emission_pro = emission_pro
        self.__transition_pro = transition_pro
        self.__observation_sqe = observation_sqe

    def predict_viterbi(self):
        """
            使用viterbi算法预测
        :return:
        """
        n = len(self.__start_pro)
        model = hmm.MultinomialHMM(n_components=n)
        model.startprob_ = self.__start_pro
        model.transmat_ = self.__transition_pro
        model.emissionprob_ = self.__emission_pro
        log_prob, result = model.decode(self.__observation_sqe, algorithm="viterbi")
        return result

    def estimation_problem(self,):
        """
         给定一个观测序列，求其最大概率
        :return: 最大概率
        """
        n = len(self.__start_pro)
        model = hmm.MultinomialHMM(n_components=n)
        model.startprob_ = self.__start_pro
        model.transmat_ = self.__transition_pro
        model.emissionprob_ = self.__emission_pro
        prob_obs = model.score(self.__observation_sqe)
        return prob_obs

