import numpy as np
import pandas as pd


def calculate_H(arr, axis):
    sum_arr = arr.sum(axis=axis)
    all_sum = sum_arr.sum()
    res = 0.0
    if axis is None:
        sum_arr = arr.copy()
    for i in sum_arr:
        p = i / all_sum
        h = p * np.log2(p)
        res -= h.sum()
    return np.round(res, decimals=2)


def calculate_rel_H(arr):
    p_y = arr.sum(axis=1) * 1.0
    all_sum = p_y.sum()
    p_y /= all_sum

    sum_x = arr.sum(axis=1)
    p_x = arr * 1.0
    res = 0.0
    for i in range(len(sum_x)):
        res_x = 0.0
        p_x[i] /= sum_x[i]
        h = p_x[i] * np.log2(p_x[i])
        res_x -= h.sum()
        res += p_y[i] * res_x
    return np.round(res, decimals=2)


def main():
    df = pd.read_csv('data.csv', sep=None, engine='python')
    df = df.select_dtypes(include=['number'])
    data = df.values
    H_ab = calculate_H(data, None)
    H_a = calculate_H(data, 1)
    H_b = calculate_H(data, 0)
    H_b_a = calculate_rel_H(data)
    assert H_b_a + H_a - H_ab <= 0.001
    I = np.round(H_b - H_b_a, decimals=2)
    return [H_ab, H_a, H_b, H_b_a, I]


print(main())
