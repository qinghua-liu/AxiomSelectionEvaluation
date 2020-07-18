import os
from joblib import Parallel, delayed
from tqdm import tqdm
from data_structure import Problem_Order
from atp import run_E_prover
from atp_with_selection import run_E_prover_with_only_selection


def process(thm, problem_dir,
            selected_problem_dir, output_dir):
    input_file = os.path.join(problem_dir, thm)
    selected_file = os.path.join(selected_problem_dir, thm)
    run_E_prover_with_only_selection(input_file, selected_file)
    output_file = os.path.join(output_dir, thm)
    run_E_prover(selected_file, output_file, 60)


if __name__ == "__main__":
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    problem_dir = "../problem/no_selection"
    selected_problem_dir = "../problem/E_selection"
    output_dir = "../E_output/E_selection"

    if not os.path.exists(selected_problem_dir):
        os.mkdir(selected_problem_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    Parallel(n_jobs=10)(delayed(process)(thm, problem_dir,
                                         selected_problem_dir,
                                         output_dir)
                        for thm in tqdm(problem_order))
