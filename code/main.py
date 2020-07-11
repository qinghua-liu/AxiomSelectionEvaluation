import os
from data_structure import Atom_Features, Symbol_Features, \
    Chronology, Problem_Order, Statements
from selection import problem_ranking, problem_weights
from utils import write_ranking_to_csv, set_recorder
from atp import proofs_from_ranking

if __name__ == "__main__":
    atom_features = Atom_Features("../data/atom_features")
    symbol_features = Symbol_Features("../data/symbol_features")
    chronology = Chronology("../data/chronology")
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    statements = Statements("../data/statements")

    ranking_dir = "../ranking"
    problem_dir = "../problem"
    output_dir = "../output"
    recorder = set_recorder("E", os.path.join(ranking_dir, "record.log"))

    for thm in [problem_order[500]]:
        available_prems = chronology.available_premises(thm)
        f_weights, v_weight = problem_weights(
            thm, available_prems, symbol_features)
        prem2score = problem_ranking(thm, available_prems,
                                     atom_features, f_weights, v_weight)
        write_ranking_to_csv(prem2score, os.path.join(ranking_dir, thm))
        proofs_from_ranking(thm, prem2score, statements,
                            problem_dir, output_dir, recorder)
