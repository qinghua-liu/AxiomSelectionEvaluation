import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from chow_test import p_value
import matplotlib.pyplot as plot

sys.path.append("../code")
from selection import scored_premises_from_csv_ranking


def split_ranking(prem2socre):
    # prems = [pair[0] for pair in prem2socre]
    scores = np.array([pair[1] for pair in prem2socre])
    last_zero_index = np.max(np.where(0.0 == scores))
    first_inf_index = np.min(np.where(float("inf") == scores))
    return scores, last_zero_index, first_inf_index


def mse_loss(socres, pred_scores):
    return np.mean((socres - pred_scores) ** 2)


def linear_regression_selection(prem2socre):
    prems = [pair[0] for pair in prem2socre]
    scores, last_zero_index, first_inf_index = split_ranking(prem2socre)
    # N = len(scores)
    # candicate_scores = scores[last_zero_index + 1: first_inf_index]
    x = np.arange(len(scores), dtype=np.float64)

    start_index = last_zero_index + 1
    end_index = first_inf_index
    stop_flag = False
    while not stop_flag:
        p_min = float("inf")
        min_cut = -1
        for i in range(start_index + 1, end_index):
            left_scores = scores[start_index: i]
            right_scores = scores[i: end_index]
            left_x = x[start_index: i]
            right_x = x[i: end_index]
            p, coeff_total, coeff_1, coeff_2 = p_value(
                left_scores, left_x, right_scores, right_x)
            print(coeff_total)
            if p < p_min:
                p_min = p
                # the last index of left part
                min_cut = i - 1
        print(p_min)
        print(min_cut)
        if p_min >= 1e-2:
            stop_flag = True
        else:
            actual_cut_index = np.max(np.where(scores[min_cut] == scores))
            print(actual_cut_index)
            end_index = actual_cut_index + 1
    actual_cut_index = np.max(np.where(scores[min_cut] == scores))
    selected_axioms = prems[: actual_cut_index + 1]
    print(len(selected_axioms))
    print(actual_cut_index)


a = scored_premises_from_csv_ranking("t47_funct_1", "../ranking")
linear_regression_selection(a)
