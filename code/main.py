import os
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm
from data_structure import Atom_Features, Symbol_Features, \
    Chronology, Problem_Order, Statements
from selection import problem_ranking, problem_weights
from utils import write_ranking_to_csv, set_recorder
from atp import E_proofs_from_ranking, Vampire_proofs_from_ranking


def set_parameters():
    params = argparse.ArgumentParser()
    params.add_argument("--ranking_dir", type=str, default="../ranking/symmetry_combine",
                        help="the root path to save ranking csv file")
    params.add_argument("--problem_dir", type=str, default="../problem/symmetry_combine",
                        help="the root path to save problems")
    params.add_argument("--E_output_dir", type=str, default="../E_output/symmetry_combine",
                        help="the root paht to save E outputs")
    params.add_argument("--Vampire_output_dir", type=str,
                        default="../Vampire_output/symmetry_combine")
    params.add_argument("--weight", type=str, default="default",
                        help="the weight for symbols, {default, frequency}")
    params.add_argument("--metric", type=str, default="symmetry",
                        help="the formula metric, args in {symmetry,weighted_average, weighed_sum, average}")
    params.add_argument("--combine", type=bool, default=True,
                        help="combine the tuple or not")
    args = params.parse_args(args=[])
    return args


def process(thm, chronology, statements, atom_features,
            symbol_features, slice_list, weight, metric, combine,
            problem_dir, E_output_dir, Vampire_output_dir, ranking_dir):
    available_prems = chronology.available_premises(thm)
    f_weights, v_weight = problem_weights(
        thm, available_prems, symbol_features, weight)
    prem2score = problem_ranking(thm, available_prems, atom_features,
                                 f_weights, v_weight, metric, combine)
    write_ranking_to_csv(prem2score, os.path.join(ranking_dir, thm))
    ranking = [pair[0] for pair in prem2score]
    E_proofs_from_ranking(thm, ranking, slice_list,
                          statements, problem_dir, E_output_dir)
    Vampire_proofs_from_ranking(thm, ranking, slice_list, statements,
                                problem_dir, Vampire_output_dir)


if __name__ == "__main__":
    atom_features = Atom_Features("../data/atom_features")
    symbol_features = Symbol_Features("../data/symbol_features")
    chronology = Chronology("../data/chronology")
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    statements = Statements("../data/statements")

    args = set_parameters()

    if not os.path.exists(args.ranking_dir):
        os.makedirs(args.ranking_dir)
    if not os.path.exists(args.problem_dir):
        os.makedirs(args.problem_dir)
    if not os.path.exists(args.E_output_dir):
        os.makedirs(args.E_output_dir)
    if not os.path.exists(args.Vampire_output_dir):
        os.makedirs(args.Vampire_output_dir)

    slice_list = [32, 64, 128, 256, 512, 1024]
    Parallel(n_jobs=10)(delayed(process)(thm, chronology, statements,
                                         atom_features, symbol_features,
                                         slice_list, args.weight,
                                         args.metric, args.combine,
                                         args.problem_dir, args.E_output_dir,
                                         args.Vampire_output_dir,
                                         args.ranking_dir)
                        for thm in tqdm(problem_order))
