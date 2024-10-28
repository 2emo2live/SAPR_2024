import json
import numpy as np


def create_matrix(order_json: str) -> np.ndarray:
    split_group = json.loads(order_json)
    split_order = order_json.replace("[", "").replace("]", "").split(',')
    n = len(split_order)
    matrix = np.zeros((len(split_order), len(split_order)), dtype=int)
    for i in range(len(split_order)):
        idx = int(split_order[i])
        for j in range(i, n):
            matrix[idx - 1, int(split_order[j]) - 1] = 1
    for eq in split_group:
        if not isinstance(eq, int):
            for ch1 in range(len(eq)):
                for ch2 in range(ch1, len(eq)):
                    matrix[int(eq[ch1]) - 1, int(eq[ch2]) - 1] = 1
                    matrix[int(eq[ch2]) - 1, int(eq[ch1]) - 1] = 1
    return matrix


def main(order_1: str, order_2: str) -> str:
    matrix_1 = create_matrix(order_1)
    matrix_2 = create_matrix(order_2)
    final_matrix = (matrix_1 * matrix_2) + (matrix_1.T * matrix_2.T)
    collision_idx = np.where(final_matrix == 0)
    collisions = []
    for i in range(len(collision_idx[0])//2):
        collisions.append([int(collision_idx[0][i]) + 1, int(collision_idx[1][i]) + 1])
    return json.dumps(collisions)


with open('A.json', 'r') as file:
    order_A = file.read()
with open('B.json', 'r') as file:
    order_B = file.read()
print(main(order_A, order_B))
