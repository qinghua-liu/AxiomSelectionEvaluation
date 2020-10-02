import os
import sys
from tqdm import tqdm

sys.path.append("..")
from data_structure import Problem_Order
from utils import read_lines


def E_proof_statistic(problem_order, output_dir):
    proofs = 0
    for name in tqdm(problem_order):
        file_path = os.path.join(output_dir, name)
        lines = read_lines(file_path)
        if "# Proof found!" in lines and "# SZS status Theorem" in lines:
            proofs += 1
    return proofs


problem_order = Problem_Order("test_theorems")
proofs = E_proof_statistic(problem_order,"/exp/home/qinghua/AxiomSelectionEvaluation-master/E_output/E_selection")
print(proofs)
