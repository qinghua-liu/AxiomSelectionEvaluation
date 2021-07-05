import os
import numpy as np
from chow_test import p_value
import matplotlib.pyplot as plt


def split_ranking(prem2socre):
    """
    @Args:
        the sorted list of pairs (prem, score)
    @Returns:
        scores: the sorted scores
        last_zero_index: the index of the last zero in the scores list
        first_inf_index: the index of the first inf in the scores list
    """
    scores = np.array([pair[1] for pair in prem2socre])
    try:
        last_zero_index = np.max(np.where(0.0 == scores))
    except:
        last_zero_index = None
    try:
        first_inf_index = np.min(np.where(float("inf") == scores))
    except:
        first_inf_index = None
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


def linear_regression_selection(prem2socre, show_figure=False):
    prems = [pair[0] for pair in prem2socre]
    scores, last_zero_index, first_inf_index = split_ranking(prem2socre)
    # N = len(scores)
    # candicate_scores = scores[last_zero_index + 1: first_inf_index]
    x = np.arange(len(scores), dtype=np.float64)

    start_index = last_zero_index + 1 if last_zero_index else 0
    end_index = first_inf_index if first_inf_index else len(prems)
    stop_flag = False
    # min_cuts = []
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
        if p_min > 1e-64:
            stop_flag = True
        else:
            if show_figure:
                plot_figure(min_left_coeff, min_right_coeff,
                            x, scores, min_cut, start_index, end_index)
            # min_cuts.append(min_cut)
            end_index = min_cut

    if min_cut > -1:
        actual_index = np.max(np.where(scores[i - 1] == scores))
        selected_prems = prems[: actual_index + 1]
    else:
        selected_prems = prems[: first_inf_index]
    # actual_cut_indexs = [
    #     np.max(np.where(scores[s - 1] == scores)) + 1 for s in min_cuts]
    # selected_prems_list = [prems[: index + 1] for index in actual_cut_indexs]
    # cut2prem = dict(zip(min_cuts, selected_prems_list))

    return selected_prems


def compute_ranking_density(thm, proofs, ranking):
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


def process_problem(thm, ranking_dir,
                    statements, problem_dir,
                    E_output_dir, Vampire_output_dir):
    prem2score = scored_premises_from_csv_ranking(thm, ranking_dir)
    ranking = linear_regression_selection(prem2score)
    input_file = os.path.join(problem_dir, thm)
    E_output_file = os.path.join(E_output_dir, thm)
    Vampire_output_file = os.path.join(Vampire_output_dir, thm)
    write_problem(thm, ranking, statements, input_file)
    run_E_prover(input_file, E_output_file, cpu_time=60)
    run_Vampire_prover(input_file, Vampire_output_file, cpu_time=60)


# def set_parameters():
#     params = argparse.ArgumentParser()
#     params.add_argument("--ranking_dir",
#                         type=str,
#                         default="../ranking/weighted_average",
#                         help="the root path to save ranking csv file")
#     params.add_argument("--problem_dir",
#                         type=str,
#                         default="../problem/weighted_average_chow_cut",
#                         help="the root path to save problems")
#     params.add_argument("--E_output_dir",
#                         type=str,
#                         default="../E_output/weighted_average_chow_cut",
#                         help="the root paht to save E outputs")
#     params.add_argument("--Vampire_output_dir",
#                         type=str,
#                         default="../Vampire_output/weighted_average_chow_cut",
#                         help="the root paht to save Vampire outputs")
#     args = params.parse_args(args=[])
#     return args


# if __name__ == "__main__":
#     statements = Statements("../data/statements")
#     problem_order = Problem_Order("../data/ProblemsInMMLOrder")

#     args = set_parameters()

#     assert os.path.exists(args.ranking_dir)
#     if not os.path.exists(args.problem_dir):
#         os.makedirs(args.problem_dir)
#     if not os.path.exists(args.E_output_dir):
#         os.makedirs(args.E_output_dir)
#     if not os.path.exists(args.Vampire_output_dir):
#         os.makedirs(args.Vampire_output_dir)

#     Parallel(n_jobs=10)(delayed(process_problem)(thm, args.ranking_dir,
#                                                  statements,
#                                                  args.problem_dir,
#                                                  args.E_output_dir,
#                                                  args.Vampire_output_dir)
#                         for thm in tqdm(problem_order))
