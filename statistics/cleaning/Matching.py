import pandas as pd

input_file_path = r"E:/NC0104/0715/Supplementary/change/Updated_A0.csv"

df = pd.read_csv(input_file_path, delimiter=',', header=None)

if df.shape[1] == 6:
    df.columns = ['Cities', 'Centrality', 'Value3', 'Value4', 'Value5', 'CulturalGroups']
else:
    raise ValueError("The number of columns in the CSV file does not match the expected value, check the file format.")

df['Centrality'] = pd.to_numeric(df['Centrality'], errors='coerce')

grouped_df = df.groupby('CulturalGroups')['Centrality'].mean().reset_index()


grouped_df.columns = ['CulturalGroups', 'AverageCentrality']

output_file_path = r"E:/NC0104/0715/Supplementary/change/CulturalGroups_AverageCentrality.csv"
grouped_df.to_csv(output_file_path, index=False)

print(f"Data have been summarized and saved to {output_file_path}")



