import sys
import os
import numpy as np
# from sklearn.linear_model import LinearRegression
from chow_test import p_value
import matplotlib.pyplot as plt
import json

sys.path.append("../code")
from selection import scored_premises_from_csv_ranking
from data_structure import Proofs


def split_ranking(prem2socre):
    # prems = [pair[0] for pair in prem2socre]
    scores = np.array([pair[1] for pair in prem2socre])
    last_zero_index = np.max(np.where(0.0 == scores))
    first_inf_index = np.min(np.where(float("inf") == scores))
    return scores, last_zero_index, first_inf_index


def mse_loss(socres, pred_scores):
    return np.mean((socres - pred_scores) ** 2)


def plot_figure(left_coeff, right_coeff,
                x, scores, min_cut, start_index, end_index):
    left_x = x[start_index: min_cut]
    right_x = x[min_cut: end_index]
    pred_left_scores = left_coeff[0] * left_x + left_coeff[1]
    pred_right_scores = right_coeff[0] * right_x + right_coeff[1]
    fig, ax = plt.subplots()
    ax.scatter(x[start_index: end_index],
               scores[start_index: end_index], marker="*")
    ax.plot(left_x, pred_left_scores, color="darkorange")
    ax.plot(right_x, pred_right_scores, color="forestgreen")
    plt.savefig(os.path.join("../figures", str(min_cut)))


def linear_regression_selection(prem2socre):
    prems = [pair[0] for pair in prem2socre]
    scores, last_zero_index, first_inf_index = split_ranking(prem2socre)
    # N = len(scores)
    # candicate_scores = scores[last_zero_index + 1: first_inf_index]
    x = np.arange(len(scores), dtype=np.float64)

    start_index = last_zero_index + 1
    end_index = first_inf_index
    stop_flag = False
    min_cuts = []
    while not stop_flag:
        p_min = float("inf")
        min_cut = -1
        # min_coeff_total = np.zeros(2)
        min_left_coeff = np.zeros(2)
        min_right_coeff = np.zeros(2)
        for i in range(start_index + 1, end_index):
            left_scores = scores[start_index: i]
            right_scores = scores[i: end_index]
            left_x = x[start_index: i]
            right_x = x[i: end_index]
            p, _, left_coeff, right_coeff = p_value(
                left_scores, left_x, right_scores, right_x)
            if p < p_min:
                p_min = p
                # the last index of left part
                min_cut = i
                min_left_coeff = left_coeff
                min_right_coeff = right_coeff
        if p_min >= 1e-18:
            stop_flag = True
        else:
            plot_figure(min_left_coeff, min_right_coeff,
                        x, scores, min_cut, start_index, end_index)
            min_cuts.append(min_cut)
            end_index = min_cut

    actual_cut_indexs = [
        np.max(np.where(scores[s - 1] == scores)) + 1 for s in min_cuts]
    selected_prems_list = [prems[: index + 1] for index in actual_cut_indexs]
    cut2prem = dict(zip(min_cuts, selected_prems_list))
    return prems, cut2prem

def compute_density(thm, proofs, ranking):

    useful_prem_list = proofs[thm]
    max_indexs = []
    for useful_prems in useful_prem_list:
        try:
            max_index = max([ranking.index(prem)
                             for prem in useful_prems])
        except:
            max_index = -1
        max_indexs.append(max_index)
    temp_densities = [(len(useful_prems) + 1) / (max_index + 2)
                      for index in max_indexs]
    density = max(temp_densities)
    print(density)
    return density


def compute_ranking_selectivity(thm, proofs, ranking):
    """
    proofs: Proofs class
    ranking_root: the dir to the ranking
    """

    useful_prem_list = proofs[thm]

    temp = []
    for useful_prems in useful_prem_list:
        max_index = max([ranking.index(prem)
                         for prem in useful_prems])

        temp.append((max_index + 2) / (len(ranking) + 1))

    density = min(temp)
    print(density)
    return density


a = scored_premises_from_csv_ranking("t12_yellow_6", "../ranking")
prems, cut2prem = linear_regression_selection(a)
proofs = Proofs("../data/dependencies_from_proofs")
compute_density("t12_yellow_6", proofs, prems)
compute_ranking_selectivity("t12_yellow_6", proofs, prems)
