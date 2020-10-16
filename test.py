import sys
import os
import json
sys.path.append("./code")
from data_structure import Proofs

# with open("/Users/liuqinghua/PHD/AxiomEvaluationResults/new_Pruney_Chainy.json","r") as f:
# 	line = f.read()
# d = json.loads(line)
# for name in d:
# 	if d[name]["premises"] == []:
# 		print(name)
# pruney = Proofs("./data/pruney").proofs

# proofs = Proofs("./data/dependencies_from_proofs").proofs


# def remove_supersets(list_of_sets):
#     '''Removes proper supersets from the list of sets'''
#     list_of_sets_clean = []
#     l = len(list_of_sets)
#     for i1 in range(l):
#         for i2 in range(l):
#             if list_of_sets[i1] > list_of_sets[i2]:
#                 break
#         else:
#         	for s in list_of_sets_clean:
#         		if list_of_sets[i1] == s:
#         			break
#         	else:
#         		list_of_sets_clean.append(list_of_sets[i1])
#     return list_of_sets_clean


# new = dict()
# for conj in pruney:
#     prem_sets = pruney[conj]
#     new[conj] = remove_supersets(prem_sets)
# for conj in proofs:
#     prem_sets = proofs[conj]
#     if conj in new:
#         doub_prem_sets = prem_sets + new[conj]
#         new[conj] = remove_supersets(doub_prem_sets)
#     else:
#         new[conj] = remove_supersets(prem_sets)
# # print(new)
# with open("./data/new_pruney", "w+") as f:
# 	for conj in new:
# 		prem_sets = new[conj]
# 		for prem_set in prem_sets:
# 			f.write(conj+":"+" ".join(list(prem_set))+"\n")

