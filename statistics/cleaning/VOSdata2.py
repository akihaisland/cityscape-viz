import pandas as pd

df1 = pd.read_csv(r"E:/NC0104/0611/707/707/NA/degree_centrality.csv")
df3 = pd.read_excel(r"E:/NC0104/0611/707/707/VOS_data/Cities.xlsx")
df2 = pd.DataFrame(columns=['id', 'label', 'x', 'y', 'cluster', 'weight<size>', 'weight<strength>', 'score<strength>'])

df2['label'] = df1['label']
df2['id'] = range(len(df2))

for i, row in df2.iterrows():
    city = row['label']
    city_row = df3[df3['label'] == city]
    if not city_row.empty:
        df2.at[i, 'x'] = city_row['lon'].values[0]
        df2.at[i, 'y'] = city_row['lat'].values[0]
df2['weight<size>'] = 1
df2['weight<strength>'] = df1['Degree Centrality'] * 10
df2['score<strength>'] = df2['weight<strength>']

df2.to_csv(r"E:/NC0104/0611/707/707/NA/NA_map.csv", index=False)



















