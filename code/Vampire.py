import os
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm

from atp import run_Vampire_prover
from data_structure import Problem_Order


def set_parameters():
    params = argparse.ArgumentParser()
    params.add_argument("--problem_dir",
                        type=str,
                        default="../problem/no_selection",
                        help="the root path to save problems")
    params.add_argument("--Vampire_output_dir",
                        type=str,
                        default="../Vampire_output/Vampire_selection_own")
    args = params.parse_args(args=[])
    return args


def process(thm, problem_dir, Vampire_output_dir):
    problem_file = os.path.join(problem_dir, thm)
    assert os.path.exists(problem_file)

    output_file = os.path.join(Vampire_output_dir, thm)
    run_Vampire_prover(problem_file, output_file, 60)


if __name__ == "__main__":

    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    args = set_parameters()

    assert os.path.exists(args.problem_dir)

    if not os.path.exists(args.Vampire_output_dir):
        os.makedirs(args.Vampire_output_dir)

    Parallel(n_jobs=10)(delayed(process)(thm, args.problem_dir,
                                         args.Vampire_output_dir)
                        for thm in tqdm(problem_order))
