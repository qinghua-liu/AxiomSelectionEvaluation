from tqdm import tqdm
import csv
import pickle
from data_structure import Chronology, Symbol_Features, Atom_Features
from distance import distance_between_formulas
from selection import problem_weights

if __name__ == "__main__":
    thm = "t12_yellow_6"
    atom_features = Atom_Features("../data/atom_features")
    symbol_features = Symbol_Features("../data/symbol_features")
    chronology = Chronology("../data/chronology")

    available_prems = chronology.available_premises(thm)
    f_weights, v_weight = problem_weights(
        thm, available_prems, symbol_features)
    problem = [thm] + available_prems
    formula2score = []
    for i, f1 in enumerate(tqdm(problem)):
        for f2 in problem[i + 1:]:
            d = distance_between_formulas(
                atom_features[f1], atom_features[f2],
                f_weights, v_weight, "symmetry", True)
            formula2score.append([f1, f2, d])
    print(len(formula2score))
    with open("../t12_yellow_6.pkl", "wb+") as f:
        pickle.dump(formula2score, f, protocol=pickle.HIGHEST_PROTOCOL)

    header = ["formula", "formula", "distance"]
    with open("../t12_yellow_6.csv", "w+") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerows(formula2score)
