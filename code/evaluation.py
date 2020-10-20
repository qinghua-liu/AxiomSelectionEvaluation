import csv
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


def extract_useful_premises_from_Vampire(lines):
    names = []
    for line in lines:
        if "file" in line:
            names.append(line.split(",")[-1][: -3])
    return names


def compute_selected_problem_from_Vampire(lines):
    names = [line.split(",")[0].replace("tff(", "")
             for line in lines if "tff" in line and "axiom" in line]
    return len(names) + 1


def compute_selected_problem_from_E(lines):
    new_lines = [line for line in lines if "fof" in line and "file" in line]
    return len(new_lines)


def ranking_precision_in_pruney(pruney, problem_dir, problem_source):
    precision = 0.0
    for name in pruney:
        problem_file = os.path.join(problem_dir, name)
        problem_lines = read_lines(problem_file)
        if problem_source == "Vampire":
            selected_names = [line.split(",")[0].replace("tff(", "")
                              for line in problem_lines
                              if "tff" in line and "axiom" in line]
        if problem_source == "E":
            selected_names = [line.split(", ")[0].replace(
                "fof(", "") for line in problem_lines
                if "fof" in line and "file" in line and "axiom" in line]
        if problem_source == "Q_selection":
            selected_names = [line.split(",")[0].replace(
                "fof(", "") for line in problem_lines
                if "fof" in line and "axiom" in line]
            print(selected_names)
        proofs = pruney[name]
        temp = [len(proof)
                for proof in proofs if proof.issubset(set(selected_names))]
        if temp:
            precision += (max(temp) + 1) / (len(selected_names) + 1)
    precision = precision / len(pruney)
    return precision


def ranking_precision(problem_dir, output_dir, ATP, problem_source):
    filenames = os.listdir(output_dir)
    precision = 0.0
    counter = 0
    for name in filenames:

        output_file = os.path.join(output_dir, name)
        lines = read_lines(output_file)
        if ATP == "E" and "# Proof found!" in lines and \
                "# SZS status Theorem" in lines:
            counter += 1
            useful_names = extract_useful_premises_from_E(lines)

            problem_file = os.path.join(problem_dir, name)
            problem_lines = read_lines(problem_file)

            if problem_source == "Vampire":
                problem_len = compute_selected_problem_from_Vampire(
                    problem_lines)
            if problem_source == "E":
                problem_len = compute_selected_problem_from_E(problem_lines)
            if problem_source == "Q_selection":
                problem_len = len(problem_lines)

            precision += len(useful_names) / problem_len

        if ATP == "Vampire" and "% Refutation found. Thanks to Tanya!" \
                in lines:
            counter += 1
            useful_names = extract_useful_premises_from_Vampire(lines)

            problem_file = os.path.join(problem_dir, name)
            problem_lines = read_lines(problem_file)

            if problem_source == "Vampire":
                problem_len = compute_selected_problem_from_Vampire(
                    problem_lines)
            if problem_source == "E":
                problem_len = compute_selected_problem_from_E(problem_lines)
            if problem_source == "Q_selection":
                problem_len = len(problem_lines)

            precision += len(useful_names) / problem_len

    precision = precision / counter
    return precision, counter


def ranking_density(proofs, rankings):

    sum_density = 0.0

    for thm_name in rankings:
        useful_prem_list = proofs[thm_name]
        ranked_premises = rankings[thm_name]

        temp = []
        for useful_prems in useful_prem_list:
            try:
                max_index = max([ranked_premises.index(prem)
                                 for prem in useful_prems])
            except:
                max_index = - 1

            temp.append((len(useful_prems) + 1) / (max_index + 2))

        sum_density += max(temp)

    density = sum_density / len(rankings)

    return density


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
    problem_dir = "/exp/home/qinghua/AxiomSelectionEvaluation-master/problem/average_inf"
    output_dir = "/exp/home/qinghua/AxiomSelectionEvaluation-master/E_output/average_inf"
    a, b = ranking_precision(problem_dir, output_dir)
    print(a)
    print(b)
