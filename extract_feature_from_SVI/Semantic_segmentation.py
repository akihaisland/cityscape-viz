import os
import tarfile               
import glob
import cv2
import numpy as np           
from PIL import Image        
import tensorflow as tf
import time                  

os.environ["TF_CPP_MIN_LOG_LEVEL"] ="2"         


class DeepLabModel(object):         

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'


    def __init__(self, tarball_path):            
        self.graph = tf.Graph()
        graph_def = None
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.compat.v1.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.compat.v1.Session(graph=self.graph)


    def run(self, image):          

        batch_seg_map = self.sess.run(self.OUTPUT_TENSOR_NAME,
                                      feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(image)]})
        seg_map = batch_seg_map[0]
        return seg_map


if __name__ == '__main__':        
    input_folder = "/teams/Landscape_1688351963/"
    output_folder = "/teams/Landscape_1688351963/"
    
    G = "Group1"  
    folder_types = ["12", "34"]  
    
    model_file = r"/teams/Landscape_1688351963/Landscape_identification/models/deeplabv3_cityscapes_train_2018_02_06.tar.gz"
    
    
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
                    t=int(time.time())
                    MODEL = DeepLabModel(model_file)

                    for filename in os.listdir(folder_path):  
                        if filename.endswith(".jpg"):  
                            try:
                                st=int(time.time())
                                count += 1  
                                orignal_im = Image.open(os.path.join(folder_path,filename))
                                seg_map = MODEL.run(orignal_im)
                                new_im = Image.fromarray(seg_map.astype('uint8'))
                                new_im.save(os.path.join(output_subfolder,filename))
                                print(count,'/',total_count)
                            except:
                                print(filename)
