import csv
import json
import os

from utils import read_lines


def select_premises_with_score_zero(ranking_file):
    with open(ranking_file, "r") as f:
        reader = csv.reader(f)
        prem2score = [row for row in reader]
    prems = [pair[0] for pair in prem2score if float(pair[1]) == 0.0]
    print(prems)
    return prems


def extract_useful_premises_from_E(lines):
    names = []
    for line in lines:
        if "fof" in line and "file" in line:
            names.append(line.split(",")[0].replace("fof(", ""))
    return names


def extract_selected_premises_from_Vampire(lines):
    names = [line.split(",")[0].replace("tff(", "")
             for line in lines if "tff" in line and "axiom" in line]
    return len(names) + 1


def ranking_precision(problem_dir, output_dir, source):
    filenames = os.listdir(output_dir)
    precision = 0.0
    counter = 0
    for name in filenames:
        output_file = os.path.join(output_dir, name)
        lines = read_lines(output_file)
        if "# Proof found!" in lines and "# SZS status Theorem" in lines:
            counter += 1
            useful_names = extract_useful_premises_from_E(lines)
            problem_file = os.path.join(problem_dir, name)
            if source == "Vampire":
                problem_len = extract_selected_premises_from_Vampire(
                    read_lines(problem_file))
            else:
                problem_len = len(read_lines(problem_file))
            precision += len(useful_names) / problem_len

    precision = precision / counter
    return precision, counter


def ranking_density(proof_file, ranking_dir):
    with open(proof_file, "r") as f:
        proof_dict = json.loads(f.read())

    enough_couner = 0
    sum_ranking_density = 0.0
    for name in proof_dict:
        thm = proof_dict[name]["conjecture"]
        ranking_file = os.path.join(ranking_dir, thm)
        selected_prems = select_premises_with_score_zero(ranking_file)

        prem_lists = \
            [prem_list for prem_list in proof_dict[name]['premises'] if set(
                prem_list).issubset(set(selected_prems))]

        if prem_lists:
            enough_couner += 1
            density_scores = []
            for prem_list in prem_lists:
                try:
                    max_prem_index = max(
                        [selected_prems.index(prem) for prem in prem_list])
                    max_position = max_prem_index + 1
                except:
                    max_position = 0
                density_scores.append(
                    (len(prem_list) + 1) / (max_position + 1))
                print(density_scores)

                sum_ranking_density += max(density_scores)

    ranking_density = sum_ranking_density / len(proof_dict)
    en_ranking_density = 0.0
    if enough_couner > 0:
        en_ranking_density = sum_ranking_density / enough_couner
    return ranking_density, en_ranking_density


def E_proof_statistic(output_dir):
    filenames = os.listdir(output_dir)
    proofs = 0
    for name in filenames:
        file_path = os.path.join(output_dir, name)
        lines = read_lines(file_path)
        if "# Proof found!" in lines and "# SZS status Theorem" in lines:
            proofs += 1
    return proofs


def Vampire_proof_statistic(output_dir):
    filenames = os.listdir(output_dir)
    proofs = 0
    for name in filenames:
        file_path = os.path.join(output_dir, name)
        lines = read_lines(file_path)
        if '% Refutation found. Thanks to Tanya!' in lines:
            proofs += 1
    return proofs


def E_proof_distribution(problem_dir, output_dir):
    filenames = os.listdir(output_dir)
    distribution = {32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0}
    for name in filenames:
        output_file = os.path.join(output_dir, name)
        lines = read_lines(output_file)
        if "# Proof found!" in lines and "# SZS status Theorem" in lines:
            problem_file = os.path.join(problem_dir, name)
            formulas = read_lines(problem_file)
            if len(formulas) - 1 <= 32:
                distribution[32] += 1
            if len(formulas) - 1 > 32 and len(formulas) - 1 <= 64:
                distribution[64] += 1
            if len(formulas) - 1 > 64 and len(formulas) - 1 <= 128:
                distribution[128] += 1
            if len(formulas) - 1 > 128 and len(formulas) - 1 <= 256:
                distribution[256] += 1
            if len(formulas) - 1 > 256 and len(formulas) - 1 <= 512:
                distribution[512] += 1
            if len(formulas) - 1 > 512 and len(formulas) - 1 <= 1024:
                distribution[1024] += 1
    return distribution


def Vampire_proof_distribution(problem_dir, output_dir):
    filenames = os.listdir(output_dir)
    distribution = {32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0}
    for name in filenames:
        output_file = os.path.join(output_dir, name)
        lines = read_lines(output_file)
        if '% Refutation found. Thanks to Tanya!' in lines:
            problem_file = os.path.join(problem_dir, name)
            formulas = read_lines(problem_file)
            if len(formulas) - 1 <= 32:
                distribution[32] += 1
            if len(formulas) - 1 > 32 and len(formulas) - 1 <= 64:
                distribution[64] += 1
            if len(formulas) - 1 > 64 and len(formulas) - 1 <= 128:
                distribution[128] += 1
            if len(formulas) - 1 > 128 and len(formulas) - 1 <= 256:
                distribution[256] += 1
            if len(formulas) - 1 > 256 and len(formulas) - 1 <= 512:
                distribution[512] += 1
            if len(formulas) - 1 > 512 and len(formulas) - 1 <= 1024:
                distribution[1024] += 1
    return distribution


if __name__ == "__main__":
    problem_dir = "/exp/home/qinghua/AxiomSelectionEvaluation-master/problem/average"
    output_dir = "/exp/home/qinghua/AxiomSelectionEvaluation-master/E_output/average"
    a, b = ranking_precision(problem_dir, output_dir)
    print(a)
    print(b)
