import os
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm

from atp import run_E_prover, run_Vampire_prover
from selection import Qinf_selection_from_csv_ranking
from utils import write_problem
from data_structure import Statements, Problem_Order


def set_parameters():
    params = argparse.ArgumentParser()
    params.add_argument("--ranking_dir",
                        type=str,
                        default="../ranking/weighted_average",
                        help="the root path to save ranking csv file")
    params.add_argument("--problem_dir",
                        type=str,
                        default="../problem/weighted_average_inf",
                        help="the root path to save problems")
    params.add_argument("--E_output_dir",
                        type=str,
                        default="../E_output/weighted_average_inf",
                        help="the root paht to save E outputs")
    params.add_argument("--Vampire_output_dir",
                        type=str,
                        default="../Vampire_output/weighted_average_inf")
    params.add_argument("--weight",
                        type=str,
                        default="default",
                        help="the weight for symbols, {default, frequency}")
    params.add_argument("--metric",
                        type=str,
                        default="symmetry",
                        help="the formula metric, args in {symmetry, weighted_average, weighed_sum, average}")
    params.add_argument("--combine", type=bool, default=False,
                        help="combine the tuple or not")
    args = params.parse_args(args=[])
    return args


def process(thm, statements, ranking_dir, problem_dir,
            E_output_dir, Vampire_output_dir):
    selected_prems = Qinf_selection_from_csv_ranking(thm, ranking_dir)
    problem_file = os.path.join(problem_dir, thm)
    write_problem(thm, selected_prems, statements, problem_file)
    E_output_file = os.path.join(E_output_dir, thm)
    Vampire_output_file = os.path.join(Vampire_output_dir, thm)
    run_E_prover(problem_file, E_output_file, 60)
    run_Vampire_prover(problem_file, Vampire_output_file, 60)


if __name__ == "__main__":

    statements = Statements("../data/statements")
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")

    args = set_parameters()

    assert os.path.exists(args.ranking_dir)
    if not os.path.exists(args.problem_dir):
        os.makedirs(args.problem_dir)
    if not os.path.exists(args.E_output_dir):
        os.makedirs(args.E_output_dir)
    if not os.path.exists(args.Vampire_output_dir):
        os.makedirs(args.Vampire_output_dir)

    Parallel(n_jobs=10)(delayed(process)(thm, statements,
                                         args.ranking_dir,
                                         args.problem_dir,
                                         args.E_output_dir,
                                         args.Vampire_output_dir)
                        for thm in tqdm(problem_order))
