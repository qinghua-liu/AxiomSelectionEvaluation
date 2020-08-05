import os
import pickle
from tqdm import tqdm
from atp import E_proofs_from_ranking
from joblib import Parallel, delayed
from data_structure import Problem_Order, Statements


def process(thm, rankings, slice_list, statements, problem_dir, output_dir):
    ranking = [pair[0] for pair in rankings[thm]]
    E_proofs_from_ranking(thm, ranking, slice_list,
                          statements, problem_dir, output_dir)


if __name__ == "__main__":
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    statements = Statements("../data/statements")
    problem_dir = "../Graph_Embedding/VGAE/input"
    output_dir = "../Graph_Embedding/VGAE/output"
    with open("../Graph_Embedding/VGAE/VGAE_0804.pkl", "r") as f:
        rankings = pickle.load(f)
    slice_list = [32, 64, 128, 256, 512, 1024]
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    Parallel(n_jobs=5)(delayed(process)(thm, rankings,
                                        slice_list, statements,
                                        problem_dir, output_dir)
                       for thm in tqdm(problem_order))
