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

input_folder = "/teams/Landscape_1688351963/Building/"
output_folder = "/teams/Landscape_1688351963/Material/"

Groupname = ["Group1"]

folder_types = ["34"]  

for G in Groupname:
    lst_name = os.listdir(input_folder + G)  
    total_count = 0  
    a = 0
    for foldername in lst_name:  
        if foldername not in ["XXX", "XXX", "XXX", "XXX"]:  
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
                            img_folder = os.path.join(output_subfolder, os.path.splitext(filename)[0])
                            os.makedirs(img_folder, exist_ok=True)
                            img_file = os.path.join(folder_path, filename)
                            image = cv2.imread(img_file)

                            h, w = image.shape[:2]

                            
                            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                            ret, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

                            
                            _, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

                            
                            for i, stat in enumerate(stats):
                                if stat[4] < 10000:
                                    labels[labels == i] = 0
                            
                            result = np.uint8(labels > 0) * 255
                            
                            window_size = (100, 100)
                            threshold = 1
                            
                            filled = result.copy()

                            h, w = binary.shape[:2]
                            
                            rectangles = []
                            centers = []
                            
                            for y in range(0, h, window_size[0]):
                                for x in range(0, w, window_size[1]):
                                    
                                    window = binary[y:y + window_size[0], x:x + window_size[1]]
                                    
                                    white_pixels = np.count_nonzero(window == 255)
                                    ratio = white_pixels / (window_size[0] * window_size[1])

                                    if ratio >= threshold:
                                        rectangles.append((x, y, x + window_size[1], y + window_size[0]))
                                        center_x = (x + x + window_size[1]) // 2
                                        center_y = (y + y + window_size[0]) // 2
                                        centers.append((center_x, center_y))

                            if len(rectangles) <= 10:
                                window_size = (80, 80)
                                
                                rectangles = []
                                centers = []
                                
                                for y in range(0, h, window_size[0]):
                                    for x in range(0, w, window_size[1]):
                                        
                                        window = binary[y:y + window_size[0], x:x + window_size[1]]

                                        white_pixels = np.count_nonzero(window == 255)
                                        ratio = white_pixels / (window_size[0] * window_size[1])
                                        
                                        if ratio >= threshold:
                                            rectangles.append((x, y, x + window_size[1], y + window_size[0]))
                                            center_x = (x + x + window_size[1]) // 2
                                            center_y = (y + y + window_size[0]) // 2
                                            centers.append((center_x, center_y))

                                if len(rectangles) <= 10:
                                    window_size = (60, 60)
                                    
                                    rectangles = []
                                    centers = []
                                    
                                    for y in range(0, h, window_size[0]):
                                        for x in range(0, w, window_size[1]):
                                            
                                            window = binary[y:y + window_size[0], x:x + window_size[1]]

                                            white_pixels = np.count_nonzero(window == 255)
                                            ratio = white_pixels / (window_size[0] * window_size[1])
                                            
                                            if ratio >= threshold:
                                                rectangles.append((x, y, x + window_size[1], y + window_size[0]))
                                                center_x = (x + x + window_size[1]) // 2
                                                center_y = (y + y + window_size[0]) // 2
                                                centers.append((center_x, center_y))

                            for i, rect in enumerate(rectangles):
                                x1, y1, x2, y2 = rect
                                length = x2 - x1  
                                center_x, center_y = centers[i]
                                cropped = image[y1:y2, x1:x2]
                                new_filename = f'cropped{i}_{length}_{center_x}_{center_y}_{os.path.splitext(filename)[0]}_{foldername}.jpg'  
                                cv2.imwrite(os.path.join(img_folder, new_filename), cropped)
                            print(filename, '__', window_size[0], '__', len(rectangles))
                            print(count,'/',total_count)
                        else:
                            continue