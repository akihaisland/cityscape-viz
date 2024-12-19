import pandas as pd
from pyproj import CRS, Transformer

file_path = r"E:/NC0104/0611/707/707/VOS_data/map.csv"
data = pd.read_csv(file_path)

wgs84 = CRS("EPSG:4326")  
web_mercator = CRS("EPSG:3857")  

transformer = Transformer.from_crs(wgs84, web_mercator, always_xy=True)

def project_coordinates(lon, lat):
    x, y = transformer.transform(lon, lat)
    return x, y

data['x_projected'], data['y_projected'] = zip(*data.apply(lambda row: project_coordinates(row['x'], row['y']), axis=1))

output_file_path = r"E:/NC0104/0611/707/707/VOS_data/map_projected.csv"
data.to_csv(output_file_path, index=False)

