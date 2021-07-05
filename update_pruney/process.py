import os
import sys
from tqdm import tqdm

sys.path.append("../code")
from data_structure import Proofs
from utils import read_lines


def change_format():
    lines = read_lines("../data/geoff_pruney.txt")
    splits = [line.split(": ") for line in lines]
    conjs = [s[0] for s in splits]
    prems = [s[1].strip() for s in splits]
    assert len(conjs) == len(prems)
    messages = [conjs[i] + ":" + prems[i] for i in range(len(conjs))]
    with open("../data/geoff_pruney", "w+") as f:
        f.write("\n".join(messages))


def remove_supersets(sets_list):

    sets_clean = []
    N = len(sets_list)
    for i1 in range(N):
        for i2 in range(N):
            if sets_list[i1] > sets_list[i2]:
                break
        else:
            sets_clean.append(sets_list[i1])
    return sets_clean


def update_pruney():
    proofs_1 = Proofs("../data/geoff_pruney")
    proofs_2 = Proofs("../data/new_pruney")
    new_proofs = proofs_2.proofs
    for conj in proofs_1:
        use_prem_l1 = proofs_1[conj]
        if conj not in new_proofs:
            new_proofs[conj] = use_prem_l1
        else:
            use_prem_l2 = proofs_2[conj]
            prem_l = []
            for prems in use_prem_l1:
                if prems not in use_prem_l2:
                    prem_l.append(prems)
            prem_l += use_prem_l2
            prem_clean = remove_supersets(prem_l)
            new_proofs[conj] = prem_clean

    messages = []
    conjs = sorted(new_proofs.keys())
    for conj in tqdm(conjs):
        prem_l = new_proofs[conj]
        print(prem_l)
        for prems in prem_l:
            message = conj + ":" + " ".join(sorted(list(prems)))
            messages.append(message)
    with open("../data/all_pruney", "w+") as f:
        f.write("\n".join(messages))


update_pruney()