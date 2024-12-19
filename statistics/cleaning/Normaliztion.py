import pandas as pd

confusion_matrix_file = r"E:/NC0104/0817/confusion_matrix_normalized.csv"
cities_cultural_file = r"E:/NC0104/0817/Cities and cultural regions.csv"
output_file = r"E:/NC0104/0817/cultural_groups_confusion_matrix_normalized_weighted.csv"

confusion_matrix = pd.read_csv(confusion_matrix_file, index_col=0)

cities_cultural = pd.read_csv(cities_cultural_file)

cultural_group_counts = cities_cultural['CULTURALGROUPS'].value_counts()

city_to_group = cities_cultural.set_index('CITIES')['CULTURALGROUPS'].to_dict()

confusion_matrix_weighted = confusion_matrix.rename(index=city_to_group, columns=city_to_group)

for group in cultural_group_counts.index:
    confusion_matrix_weighted.loc[group] /= cultural_group_counts[group]
    confusion_matrix_weighted[group] /= cultural_group_counts[group]

cultural_group_matrix = confusion_matrix_weighted.groupby(level=0).sum().groupby(axis=1, level=0).sum()

row_sums = cultural_group_matrix.sum(axis=1, numeric_only=True)
row_sums = row_sums.replace(0, 1)  
cultural_group_matrix_normalized = cultural_group_matrix.div(row_sums, axis=0).round(2)

cultural_group_matrix_normalized.to_csv(output_file)
