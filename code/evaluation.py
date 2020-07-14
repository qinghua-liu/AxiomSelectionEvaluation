import csv
import json
import os


def select_premises_with_score_zero(ranking_file):
    with open(ranking_file, "r") as f:
        reader = csv.reader(f)
        prem2score = [row for row in reader]
    prems = [pair[0] for pair in prem2score if float(pair[1]) == 0.0]
    print(prems)
    return prems


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
