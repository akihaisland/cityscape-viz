import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt

cityscapes_path = r"E:/NC0104/0729/mantel_test/MATRIX_cityscapes.csv"
cityscapes_df = pd.read_csv(cityscapes_path, index_col=0)

cities_order_path = r"E:/NC0104/0729/mantel_test/Hierarchical_Clustering.csv"
cities_order_df = pd.read_csv(cities_order_path)
cities_order = cities_order_df['Cities1'].tolist()

cityscapes_df = cityscapes_df.reindex(index=cities_order, columns=cities_order)
cityscapes_df = cityscapes_df.iloc[::-1, ::-1]

distance_matrix = 1 - cityscapes_df.values

condensed_distance_matrix = squareform(distance_matrix)

Z = linkage(condensed_distance_matrix, method='ward')
clusters_10 = fcluster(Z, 10, criterion='maxclust')


city_cluster_map = dict(zip(cityscapes_df.index.tolist(), clusters_10))
sorted_cities_order = sorted(cityscapes_df.index.tolist(), key=lambda city: city_cluster_map[city])

for k in range(10, 0, -1):
    plt.figure(figsize=(12, 8))
    dendrogram(
        Z,
        labels=sorted_cities_order,
        orientation='left',
        truncate_mode='lastp',
        p=k
    )
    plt.title(f'Hierarchical Clustering Dendrogram (k={k})')
    plt.ylabel('Distance')
    plt.xlabel('Cities')
    plt.show()
