import os
import cv2
import numpy as np
import pandas as pd

def map_hsv_to_bin(h, s, v, bins_per_channel):
    
    h = int((h / 179.0) * 255.0)
    h_bin = int(h // (256 / bins_per_channel[0]))
    s_bin = int(s // (256 / bins_per_channel[1]))
    v_bin = int(v // (256 / bins_per_channel[2]))
    return h_bin, s_bin, v_bin

input_folder = "/teams/Landscape_1688351963/color"
output_folder = "/teams/Landscape_1688351963/color_results"

G = "Group1"  
folder_types = ["34"]  
bins_per_channel = (16, 16, 16)  
total_bins = np.prod(bins_per_channel)
value_threshold = 40  
resize_dim = (128, 128)  

lst_name = os.listdir(os.path.join(input_folder, G))

for foldername in lst_name:
    if foldername not in ["XXX"]:  
        for folder_type in folder_types:
            full_input_folder = os.path.join(input_folder, G, foldername, folder_type)
            if os.path.isdir(full_input_folder):
                full_output_folder = os.path.join(output_folder, G, foldername, folder_type) 

                os.makedirs(full_output_folder, exist_ok=True)

                column_names = ['Image', 'ID', 'Lat', 'Lon', 'Dir', 'Num_pixel'] + [f'Bin_{i}' for i in range(total_bins)]
                df = pd.DataFrame(columns=column_names)  

                for filename in os.listdir(full_input_folder):
                    if filename.endswith('.jpg'):
                        
                        ID, lat, lon, dir = filename.rsplit('.', 1)[0].split('_')
                        image_path = os.path.join(full_input_folder, filename)
                        
                        image = cv2.imread(image_path)
                        
                        resized_image = cv2.resize(image, resize_dim, interpolation=cv2.INTER_AREA)
                        
                        hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
                        
                        color_distribution = np.zeros(np.prod(bins_per_channel))
                        
                        num_valid_pixels = 0
                        
                        for i in range(hsv_image.shape[0]):
                            for j in range(hsv_image.shape[1]):
                                h, s, v = hsv_image[i, j]
                                if v > value_threshold:  
                                    bin_indices = map_hsv_to_bin(h, s, v, bins_per_channel)
                                    bin_index = np.ravel_multi_index(bin_indices, bins_per_channel)
                                    color_distribution[bin_index] += 1
                                    num_valid_pixels += 1
                        
                        color_probabilities = color_distribution / color_distribution.sum() if num_valid_pixels > 0 else np.zeros(total_bins)
                        
                        data_row = [filename, ID, lat, lon, dir, num_valid_pixels] + list(color_probabilities)
                        df_length = len(df)
                        df.loc[df_length] = data_row

                csv_path_mid = os.path.join(output_folder, G, foldername, f'{foldername}_color_raw.csv')
                df.to_csv(csv_path_mid, index=False)
                
                df = pd.read_csv(csv_path_mid)

                bin_columns = [col for col in df.columns if col.startswith('Bin_')]
                
                group_columns = ['ID', 'Lat', 'Lon']
                
                group_sizes = df.groupby(group_columns).size()
                
                single_rows_groups = group_sizes[group_sizes == 1].index
                
                df1 = df.set_index(group_columns).loc[single_rows_groups].reset_index()
                
                df1.drop(columns=['Image', 'Dir', 'Num_pixel'], inplace=True)
                
                multiple_rows_groups = group_sizes[group_sizes > 1].index
                
                df_to_merge = df.set_index(group_columns).loc[multiple_rows_groups].reset_index()
                
                def weighted_average(sub_df):
                    weights = sub_df['Num_pixel']
                    weighted_bins = sub_df[bin_columns].multiply(weights, axis="index").sum() / weights.sum()
                    return pd.Series(weighted_bins, index=bin_columns)
                
                df2 = df_to_merge.groupby(group_columns).apply(weighted_average).reset_index()

                df_final = pd.concat([df1, df2], ignore_index=True)

                csv_path = os.path.join(output_folder, G, foldername, f'{foldername}_color.csv')
                
                df_final.to_csv(csv_path, index=False)

