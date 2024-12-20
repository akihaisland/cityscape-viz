import os
import csv
from PIL import Image
import numpy as np
count = 0
if __name__ == '__main__':        
    input_folder = "/teams/Landscape_1688351963/"
    output_folder = "/teams/Landscape_1688351963/"
    G = "Group1"  
    folder_types = ["12", "34"]  
    
    lst_name = os.listdir(input_folder + G)  
    total_count = 0  
    
    for foldername in lst_name:  
        if foldername not in ["XXX"]:
            for folder_type in folder_types:  
                if os.path.isdir(os.path.join(input_folder + G, foldername, folder_type)):
                    folder_path = os.path.join(input_folder + G, foldername, folder_type)  
                    output_subfolder = os.path.join(output_folder, G, foldername, folder_type)  
                    os.makedirs(output_subfolder, exist_ok=True)  
                    
                    writer = csv.writer(open(output_subfolder + '/' + foldername + '_' + folder_type + '_semantic_statistics.csv', "w", newline=""), dialect=("excel"))

                    
                    writer.writerow(["ID","lat","long","dir","city", "road", "sidewalk", "building", "wall", "fence",
                                     "pole", "traffic_light", "traffic_sign", "vegetation", "terrain",
                                     "sky", "person", "rider", "car", "truck", "bus", "train", "motorcycle", "bicycle", "Street_Scale"])

                    for file in os.listdir(folder_path):

                        if file.count("_") != 3:
                            continue

                        ID, lat, long, di = file.split("_")[:4]
                        img = Image.open(os.path.join(folder_path, file))
                        
                        count += 1
                        
                        count_dic = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
                                     7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                                     14: 0, 15: 0, 16: 0, 17: 0, 18: 0, -1: 0, 255: 0}
                        
                        ar = np.array(img).flatten().tolist()
                        
                        for item in count_dic:
                            count_dic[item] = ar.count(item)
                        
                        sumcount = len(ar)
                        
                        writer.writerow([ID,lat,long,os.path.splitext(di)[0],foldername, count_dic[0]*1.0/sumcount, count_dic[1]*1.0/sumcount, count_dic[2]*1.0/sumcount,
                                         count_dic[3]*1.0/sumcount, count_dic[4] * 1.0 / sumcount, count_dic[5]*1.0/sumcount,
                                         count_dic[6]*1.0/sumcount, count_dic[7]*1.0/sumcount, count_dic[8] * 1.0 / sumcount,
                                         count_dic[9]*1.0/sumcount, count_dic[10]*1.0/sumcount, count_dic[11]*1.0/sumcount,
                                         count_dic[12]*1.0/sumcount, count_dic[13] * 1.0 / sumcount, count_dic[14]*1.0/sumcount,
                                         count_dic[15]*1.0/sumcount, count_dic[16]*1.0/sumcount, count_dic[17]*1.0/sumcount,
                                         count_dic[18]*1.0/sumcount, 1.0-(count_dic[10]*1.0/sumcount)])
                        
                        print(ID, count)
                    print('finished:', foldername, '_', folder_type)
    




































