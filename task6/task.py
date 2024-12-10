import json


def fuzzification(x0, tmp_set):
    idx = 0
    mu = tmp_set["points"]
    while x0 > mu[idx][0]:
        idx += 1
        if idx >= len(mu):
            return mu[idx - 1][1]
    if (idx == 0) and (x0 < mu[idx][0]):
        return 0
    elif idx == 0:
        if mu[idx][0] == mu[idx + 1][0]:
            return mu[idx + 1][1]
        return mu[idx][1]
    return (x0 - mu[idx - 1][0]) / (mu[idx][0] - mu[idx - 1][0]) * (mu[idx][1] - mu[idx - 1][1]) + mu[idx - 1][1]


def fuzz_all(x, t_sets):
    res = []
    for C in t_sets:
        temp = (fuzzification(x, C), C["id"])
        res.append(temp)
    return res


def transfer(transf_sets, rule):
    C_sets = []
    for C in transf_sets:
        for r in rule:
            if C[1] == r[0]:
                temp = (C[0], r[1])
                C_sets.append(temp)
                break
    return C_sets


def defuzzification(C_sets, ctr_sets):
    max_pair = max(C_sets, key=lambda x: x[0])
    ctr_set = {}
    for s in ctr_sets:
        if max_pair[1] == s['id']:
            ctr_set = s
    if len(ctr_set) == 0:
        return -1
    mu = ctr_set["points"]
    idx = 0
    y = max_pair[0]
    while y > mu[idx][1]:
        idx += 1
        if idx >= len(mu):
            return -1
    if idx == 0:
        return mu[idx][0]
    return (y - mu[idx-1][1]) / (mu[idx][1] - mu[idx-1][1]) * (mu[idx][0] - mu[idx-1][0]) + mu[idx-1][0]


def main(temperature_json, control_json, rule_json, t):
    temperature = json.loads(temperature_json)
    temperature = temperature["температура"]
    control = json.loads(control_json)
    control = control["температура"]
    rule = json.loads(rule_json)

    sets = fuzz_all(t, temperature)
    tr_sets = transfer(sets, rule)
    return defuzzification(tr_sets, control)


with open('функции-принадлежности-температуры.json', 'r', encoding='utf-8') as file:
    temp_json = file.read()
with open('функции-принадлежности-управление.json', 'r', encoding='utf-8') as file:
    ctr_json = file.read()
with open('функция-отображения.json', 'r', encoding='utf-8') as file:
    r_json = file.read()

print(main(temp_json, ctr_json, r_json, 15))
