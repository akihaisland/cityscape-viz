import time
from PIL import Image
import math
import cv2
import os.path
import numpy as np
import matplotlib.pyplot as plt
import glob

def gamma_trans(img, gamma):  
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  
    return cv2.LUT(img, gamma_table)  

input_folder = "/teams/Landscape_1688351963/GVI/"  
output_folder = "/teams/Landscape_1688351963/"  

G = "Group1"  
folder_types = ["12", "34"]  

lst_name = os.listdir(input_folder + G)  
total_count = 0  

for foldername in lst_name:  
    if foldername not in ["XXX", "XXX"]:
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
                        image = cv2.imread(os.path.join(folder_path, filename))  
                        h, w = image.shape[:2]

                        K = np.array([[800, 0, w/2], [0, 800, h/2], [0, 0, 1]], dtype=np.float32)
                        D = np.array([-0.05, 0.05, -0.025, 0.025], dtype=np.float32)

                        new_image = cv2.fisheye.undistortImage(image, K, D, Knew=K)

                        cv2.imwrite(os.path.join(output_subfolder, filename), new_image)  
                        print(count, '/', total_count)  
                total_count += count  
            else:
                continue