import sys
import csv
from tqdm import tqdm

sys.path.append("../code")
from utils import read_lines
from distance import distance_between_formulas
from data_structure import Atom_Features, Symbol_Features


def problem_weights(names, symbol_features):
    symbol_set = set()
    for name in names:
        symbol_set.update(symbol_features[name])
    f_weights = dict(zip(list(symbol_set), [2.0] * len(symbol_set)))
    v_weight = 1.0
    return f_weights, v_weight


if __name__ == "__main__":
    names = read_lines("./t12_yellow_6") + ["t12_yellow_6"]
    symbol_features = Symbol_Features("../data/symbol_features")
    atom_features = Atom_Features("../data/atom_features")
    f_weights, v_weight = problem_weights(names, symbol_features)
    records = []
    for i, n1 in enumerate(tqdm(names)):
        for n2 in names[i + 1:]:
            d = distance_between_formulas(
                atom_features[n1], atom_features[n2],
                f_weights, v_weight, "symmetry", True)
            records.append((n1, n2, d))
    with open("./results.csv", "w+") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(records)
