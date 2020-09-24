import sys
import numpy as np
from sklearn.linear_model import LinearRegression

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
    min_loss = float("inf")
    min_cut = -1
    flag = True
    start_index = last_zero_index + 1
    end_index = first_inf_index - 1
    while flag:
        for i in range(start_index, end_index):
            left_scores = scores[:i].reshape(-1, 1)
            right_scores = scores[i: end_index].reshape(-1, 1)
            left_x = x[:i].reshape(-1, 1)
            right_x = x[i: end_index].reshape(-1, 1)
            left_regression = LinearRegression(
                fit_intercept=True, normalize=True).fit(left_x, left_scores)
            right_regression = LinearRegression(
                fit_intercept=True, normalize=True).fit(right_x, right_scores)
            pred_left_scores = left_regression.predict(left_x)
            pref_right_scores = right_regression.predict(right_x)
            loss = (mse_loss(left_scores, pred_left_scores)
                    + mse_loss(right_scores, pref_right_scores)) / 2
            if loss < min_loss:
                min_loss = loss
                min_cut = i - 1

        cut_score = scores[min_cut]
        actual_cut_index = np.max(np.where(cut_score == scores))
        # print(actual_cut_index)
        selected_axioms = prems[: actual_cut_index + 1]
        # print(len(selected_axioms))
        if len(selected_axioms) <= 300:
            flag = False
        else:
            end_index = actual_cut_index
    print(min_cut)
    print(actual_cut_index)
    print(len(selected_axioms))


a = scored_premises_from_csv_ranking("t47_funct_1", "../ranking")
linear_regression_selection(a)
