from distance import distance_between_formulas, compute_noninfinity


def problem_weights(theorem, available_prems, symbol_features, weight="default"):
    if weight == "default":
        symbol_set = set()
        for name in available_prems + [theorem]:
            symbol_set.update(symbol_features[name])

        f_weights = dict(zip(list(symbol_set), [2.0] * len(symbol_set)))
        v_weight = 1.0
        return f_weights, v_weight
    if weight == "frequency":
        symbol2frequency = dict()
        for name in available_prems + [theorem]:
            for sym in set(symbol_features[name]):
                if not sym in symbol2frequency:
                    symbol2frequency[sym] = 1
                else:
                    symbol2frequency[sym] += 1
        f_weights = {
            sys: symbol2frequency[sys] / (len(available_prems) + 1)
            for sys in symbol2frequency}
        v_weight = sum(list(f_weights.values())) / len(f_weights)
        return f_weights, v_weight


def problem_ranking(theorem, available_prems, atom_features,
                    f_weights, v_weight, metric, combine):
    distances = []
    for prem in available_prems:
        d = distance_between_formulas(
            atom_features[prem], atom_features[theorem],
            f_weights, v_weight, metric, combine)
        distances.append(d)

    prem2score = dict(zip(available_prems, distances))
    sorted_prem2score = sorted(prem2score.items(), key=lambda x: x[1])
    return sorted_prem2score


def Qinf_selection(sorted_prem2score):
    scores = [pair[1] for pair in sorted_prem2score]
    prems = [pair[0] for pair in sorted_prem2score]
    non_inf_num = compute_noninfinity(scores)
    selected_prems = prems[: non_inf_num]
    return selected_prems
