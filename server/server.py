import os
from helper import Helper
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.image as mpimg
from flask import Flask, request,jsonify
from tensorflow.keras.applications import InceptionResNetV2
from flask_cors import CORS
import base64
import cv2
import pickle
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
path_of_dict = r'D:\TASK\server\features_dict.pickle'
help = Helper(InceptionResNetV2,path_of_dict)
dict_fetures = help.loaded_dict
print(f"========== {help.backBone.name} ==========")
print(f"========== we have {len(dict_fetures)} items in dict ==========")


@app.route('/verify', methods=['POST'])
def add_message():
    # Get the message data from the request
    # Check if an image was provided
    if 'image' not in request.json:
        return 'No image found in the request'

    # Read the images from the request
    encoded_images = request.json['image'].split(',')[1]
    print(f"============= {len(encoded_images)} ===============")
    
    decoded_image = help.preprocess_image(encoded_images)
    print(f"type is {type(decoded_image)} , shape ===== {decoded_image.shape}")
    
    similar = help.get_Similarsites_fromDict(decoded_image,dict_fetures)
    print(len(similar))
    similar  = similar[:9]
    paths_list = [item[1] for item in similar]
    
    return jsonify({'data': paths_list})

    

if __name__ == '__main__':
    app.run(host='0.0.0.0')

