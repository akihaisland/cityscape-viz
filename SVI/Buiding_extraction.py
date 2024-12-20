import os
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
from PIL import Image

input_folder = "/teams/Landscape_1688351963/"  
output_folder = "/teams/Landscape_1688351963/Building"  

Groupname = ["Group" + str(i) for i in range(1, 2)]

folder_types = ["34"]  

for G in Groupname:
    lst_name = os.listdir(input_folder + G)  
    total_count = 0  
    a = 0
    for foldername in lst_name:  
        if foldername not in ["XXX"]:  
            for folder_type in folder_types:  
                if os.path.isdir(os.path.join(input_folder + G, foldername, folder_type)):  
                    folder_path = os.path.join(input_folder + G, foldername, folder_type)  
                    output_subfolder = os.path.join(output_folder, G, foldername, folder_type)  
                    os.makedirs(output_subfolder, exist_ok=True)  
                    jpg_files = glob.glob(folder_path + "/*.jpg")
                    total_count = len(jpg_files)
                    count = 0  

                    for filename in os.listdir(folder_path):  
                            if filename.endswith(".jpg"):  
                                count += 1  
                                input_image_path = os.path.join(folder_path, filename)

                                image1 = cv2.imread(input_image_path)  
                                image2 = cv2.imread(input_image_path)
                                
                                k = np.ones((30, 30), np.uint8)
                                image1 = cv2.morphologyEx(image1, cv2.MORPH_CLOSE, k)

                                gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

                                pixels_8 = np.where(gray_image1 == 2)
                                
                                masked_image = np.zeros_like(image2)

                                
                                masked_image[pixels_8] = image2[pixels_8]


                                non_black_pixels = np.count_nonzero(masked_image)
                                total_pixels = masked_image.shape[0] * masked_image.shape[1] * 3
                                non_black_pixel_ratio = non_black_pixels / total_pixels

                                
                                if non_black_pixel_ratio > 0.1:
                                    
                                    cv2.imwrite(output_folder + '/' + G + '/' + foldername + '/' + folder_type + '/' + filename, masked_image)
                                    a = a + 1
                                    print(count, "/", total_count)
                                else:
                                    print("Limited facade:", output_folder + '/' + filename)
                            else:
                                print("File path does not exist OR is not in jpg format:", input_image_path)