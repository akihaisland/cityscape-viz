import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.stats import pearsonr

def mantel_test(matrix1, matrix2, perms=10000):
    dist1 = squareform(matrix1, checks=False)
    dist2 = squareform(matrix2, checks=False)
    r_original, _ = pearsonr(dist1, dist2)
    permuted_rs = []
    for _ in range(perms):
        np.random.shuffle(dist2)
        r, _ = pearsonr(dist1, dist2)
        permuted_rs.append(r)
    permuted_rs = np.array(permuted_rs)
    p_value = np.sum(permuted_rs >= r_original) / perms
    return r_original, p_value

cityscapes_path = r"E:/NC0104/0729/mantel_test/MATRIX_cityscapes.csv"
cultural_groups_path = r"E:/NC0104/0729/mantel_test/MATRIX_continents.csv"

cityscapes_df = pd.read_csv(cityscapes_path, index_col=0)
cultural_groups_df = pd.read_csv(cultural_groups_path, index_col=0)

assert list(cityscapes_df.index) == list(cultural_groups_df.index)
assert list(cityscapes_df.columns) == list(cultural_groups_df.columns)

cityscapes_dist = pdist(cityscapes_df.values)
cultural_groups_dist = pdist(cultural_groups_df.values)

cityscapes_dist_matrix = squareform(cityscapes_dist)
cultural_groups_dist_matrix = squareform(cultural_groups_dist)


mantel_stat, p_value = mantel_test(cityscapes_dist_matrix, cultural_groups_dist_matrix, perms=10000)

print(f"Mantel statistic: {mantel_stat}")
print(f"P-value: {p_value}")