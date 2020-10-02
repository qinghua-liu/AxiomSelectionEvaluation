import sys
import os
import csv
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm

sys.path.append("../code")
from atp import E_proofs_from_ranking
from data_structure import Statements, Problem_Order


def extract_ranked_premises(file_path):
    with open(file_path, "r") as f:
        csv_reader = csv.reader(f)
        rows = [pair for pair in csv_reader]
    prems = [row[0] for row in rows]
    return prems


def prove_problem(thm, ranking_dir, slice_list,
                  statements, problem_dir, output_dir):
    csv_file_path = os.path.join(ranking_dir, thm)
    ranking = extract_ranked_premises(csv_file_path)
    E_proofs_from_ranking(thm, ranking, slice_list,
                          statements, problem_dir,
                          output_dir)


def set_parameters():
    params = argparse.ArgumentParser()
    params.add_argument("--ranking_dir",
                        type=str,
                        default="../cross_graph_results/ranking",
                        help="the root path to save ranking csv file")
    params.add_argument("--problem_dir",
                        type=str,
                        default="../cross_graph_results/problem",
                        help="the root path to save problems")
    params.add_argument("--output_dir",
                        type=str,
                        default="../cross_graph_results/output",
                        help="the root paht to save E outputs")
    args = params.parse_args(args=[])
    return args


if __name__ == "__main__":
    statements = Statements("../data/statements")
    problem_order = Problem_Order("test_theorems")

    args = set_parameters()

    assert os.path.exists(args.ranking_dir)
    if not os.path.exists(args.problem_dir):
        os.makedirs(args.problem_dir)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    slice_list = [32, 64, 128, 256, 512, 1024]
    Parallel(n_jobs=10)(delayed(prove_problem)(thm, args.ranking_dir,
                                               slice_list,
                                               statements,
                                               args.problem_dir,
                                               args.output_dir)
                        for thm in tqdm(problem_order))
