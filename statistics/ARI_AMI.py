import pandas as pd
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
import matplotlib.pyplot as plt

file_path = r"E:/NC0104/0729/mantel_test/Hierarchical_Clustering.csv"
df = pd.read_csv(file_path)

cities_cluster = df[['Cities1', 'Cluster_10']].set_index('Cities1').to_dict()['Cluster_10']
cities_culture = df[['Cities2', 'CulturalGroups']].set_index('Cities2').to_dict()['CulturalGroups']

common_cities = set(cities_cluster.keys()) & set(cities_culture.keys())

cluster_labels = [cities_cluster[city] for city in common_cities]
culture_labels = [cities_culture[city] for city in common_cities]

ari_score = adjusted_rand_score(cluster_labels, culture_labels)
print(f"Adjusted Rand Index (ARI) between hierarchical clustering (K=10) and CulturalGroups: {ari_score:.4f}")
ami_score = adjusted_mutual_info_score(cluster_labels, culture_labels)
print(f"Adjusted Mutual Information (AMI) between hierarchical clustering (K=10) and CulturalGroups: {ami_score:.4f}")

#Next phase
cities_culture = df[['Cities2', 'CulturalGroups']].set_index('Cities2').to_dict()['CulturalGroups']
ari_scores = []
ami_scores = []
k_values = range(2, 11)
for k in k_values:
    cluster_column = f'Cluster_{k}'
    cities_cluster = df[['Cities1', cluster_column]].set_index('Cities1').to_dict()[cluster_column]
    common_cities = set(cities_cluster.keys()) & set(cities_culture.keys())

    cluster_labels = [cities_cluster[city] for city in common_cities]
    culture_labels = [cities_culture[city] for city in common_cities]
    
    ari_score = adjusted_rand_score(cluster_labels, culture_labels)
    ami_score = adjusted_mutual_info_score(cluster_labels, culture_labels)
    
    ari_scores.append(ari_score)
    ami_scores.append(ami_score)

plt.figure(figsize=(10, 6))
plt.plot(k_values, ari_scores, marker='o', label='ARI')
plt.plot(k_values, ami_scores, marker='o', label='AMI')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Score')
plt.title('ARI and AMI Scores vs Number of Clusters (k)')
plt.legend()
plt.grid(True)
plt.show()
