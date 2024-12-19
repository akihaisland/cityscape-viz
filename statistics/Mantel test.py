import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def mantel_test(matrix1, matrix2, perms=10000):

    dist1 = matrix1[np.triu_indices_from(matrix1, k=1)]
    dist2 = matrix2[np.triu_indices_from(matrix2, k=1)]

    r_original, _ = pearsonr(dist1, dist2)

    permuted_rs = []
    for _ in range(perms):
        shuffled_dist2 = np.random.permutation(dist2)
        r, _ = pearsonr(dist1, shuffled_dist2)
        permuted_rs.append(r)

    permuted_rs = np.array(permuted_rs)

    p_value = (np.sum(permuted_rs >= r_original) + 1) / (perms + 1)

    return r_original, p_value

cityscapes_path = r"E:/NC/0729/mantel_test/MATRIX_cityscapes.csv"
cultural_groups_path = r"E:/NC/0729/mantel_test/MATRIX_continents.csv"

cityscapes_df = pd.read_csv(cityscapes_path, index_col=0)
cultural_groups_df = pd.read_csv(cultural_groups_path, index_col=0)

assert list(cityscapes_df.index) == list(cultural_groups_df.index)
assert list(cityscapes_df.columns) == list(cultural_groups_df.columns)

cityscapes_matrix = cityscapes_df.values
cultural_groups_matrix = cultural_groups_df.values

mantel_stat, p_value = mantel_test(cityscapes_matrix, cultural_groups_matrix, perms=10000)

print(f"Mantel statistic: {mantel_stat}")
print(f"P-value: {p_value}")
