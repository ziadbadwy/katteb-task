import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.applications import InceptionResNetV2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.image as mpimg
import os
import base64
import cv2
import pickle
class Helper:
    def __init__(self,backBone,dict_features_path):

        self.backBone = backBone(include_top=False, weights='imagenet', input_shape=(224, 224, 3),pooling='max')
        with open(dict_features_path, "rb") as file:
            self.loaded_dict = pickle.load(file)
    

    """def preprocess_image(self,encoded_img):
        # Decode the base64-encoded image
        decoded_image = base64.b64decode(encoded_img)
        image = tf.image.decode_jpeg(decoded_image, channels=3)  # Adjust channels if necessary
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize(image, (224, 224))  # Adjust target size if necessary
        return image.numpy()  # Convert to NumPy array
       """
    def preprocess_image(self, image_b64):
        # Decode the image
        image_bytes = base64.b64decode(image_b64)
        
        #image_string = tf.io.read_file(image_b64)
        img = tf.image.decode_jpeg(image_bytes, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = tf.image.resize(img, (224,224))
        return img
    def preprocess_local_images(self,filePath):
        """
        Load the specified file as a JPEG image, preprocess it and
        resize it to the target shape.
        """

        image_string = tf.io.read_file(filePath)
        image = tf.image.decode_jpeg(image_string, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize(image, (224,224))
        return image

  
    
    def get_fetures(self,image):
        image = np.expand_dims(image, axis = 0)
        print(f"================================{image.shape}===================")
        embedding_img = self.backBone.predict(image)
        return embedding_img
    
    def get_Score(self,client_image,local_image):
        #load images and preprocessing
        f1 = self.get_fetures(client_image)
        f2 = self.get_fetures(local_image)
        score = cosine_similarity(f1, f2)
        return score
    
    def display_image(self,image_path):
        image = mpimg.imread(image_path)
        plt.imshow(image)
        
    def get_all_paths(self,data_path):
        allPaths = lambda path: os.path.join(data_path,path)
        listOfPaths = list(map(allPaths,os.listdir(data_path)))
        return listOfPaths

    def accuracy(self,listOfPaths):
        scores = []
        for i in range(0,len(listOfPaths)-1,2):
            embedding = self.get_Score(listOfPaths[i],listOfPaths[i+1])[0][0]
            if embedding > 0.7:
                scores.append(1)
            else:
                scores.append(0)
        accuracy_score = np.average(scores)  
        return accuracy_score * 100
    
    def get_Similarsites(self,inp_img,listOfPaths):
        similarsites = []
        for img in listOfPaths:
            preprocessed_img = self.preprocess_local_images(img)
            embedding = self.get_Score(inp_img,preprocessed_img)[0][0]
            if embedding > 0.7:
                similarsites.append(img)
                
        return similarsites
    def get_dict_of_fetures(self,listOfPaths):
        dict_fetures = {}
        i = 1
        for path in listOfPaths:
            print(path)
            img = self.preprocess_image(path)
            fetures = self.get_fetures(img)
            dict_fetures[path] = fetures
            print(f"iter number : {i}")
            i+=1
        return dict_fetures
    def get_Score_fromDict(self,img,fetures_fromDict):
        score = cosine_similarity(img, fetures_fromDict)
        return score
    def get_Similarsites_fromDict(self,img,dict_of_features):
        similarsites = []
        f = self.get_fetures(img)
        for path , fetures in dict_of_features.items():
            embedding = self.get_Score_fromDict(f,fetures)[0][0]
            if embedding > 0.78:
                similarsites.append((embedding,path))
        similarsites = list(reversed(sorted(similarsites, key=lambda x: x[0])))       
        return similarsites
    
    
    
    
       

        