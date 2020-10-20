from data_structure import Proofs
from evaluation import ranking_precision_in_pruney


pruney = Proofs("../data/new_pruney")
problem_dir = "/exp/home/qinghua/AxiomSelectionEvaluation-master/problem/E_selection"

score = ranking_precision_in_pruney(pruney, problem_dir, "E")
print(score)
